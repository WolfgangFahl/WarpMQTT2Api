"""
Created on 09.05.2025

@author: wf
"""

import argparse
import json
import logging
import sys
from argparse import Namespace
from dataclasses import dataclass
from datetime import datetime

from lodstorage.yamlable import lod_storable

from warp.mqtt_client import MqttClient
from warp.mqtt_config import MqttConfig
from warp.warp3_api import Warp3Api


@dataclass
class MeterReading:
    kWh_in: float
    kWh_out: float
    time_stamp: str

    @property
    def time(self) -> datetime:
        """Convert timestamp string to datetime object"""
        return datetime.strptime(self.time_stamp, "%Y-%m-%dT%H:%M:%S")

    def active_power(self, prev: "MeterReading") -> float:
        """
        calculate the active power
        """
        # Time difference in hours
        time_delta = (self.time - prev.time).total_seconds() / 3600
        # Energy change (kWh)
        energy_delta = (self.kWh_in - prev.kWh_in) - (self.kWh_out - prev.kWh_out)

        # Power in watts
        active_power = (energy_delta * 1000) / time_delta
        return round(active_power)


@lod_storable
class WallboxConfig:
    """Configuration for the Warp3 wallbox"""

    wallbox_host: str = "http://warp3.mydomain"
    # example Tasmota reading
    power_tag: str = "eHZ"  # json tag for the payload content
    in_field: str = "E_in"  # field for energy input
    out_field: str = "E_out"  # field for energy output
    time_field: str = "Time"  # field for timestamp
    meter_id: int = 2  # id of the meter configured

    @classmethod
    def ofArgs(cls, args: Namespace = None):
        """
        Create a configuration from command line arguments.

        Args:
            args: Optional list of command line arguments. If None, sys.argv is used.

        Returns:
            WallboxConfig: Configuration object
        """
        if args is None:
            config = cls()
        else:
            config = cls(
                wallbox_host=args.wallbox_host,
                power_tag=args.power_tag,  # Added this
                in_field=args.in_field,  # Added new field
                out_field=args.out_field,  # Added new field
                time_field=args.time_field,  # Added new field
                meter_id=args.meter_id,  # Added this
            )
        return config

    @classmethod
    def addArgs(cls, parser):
        """
        Add command line arguments for WallboxConfig to the given parser.

        Args:
            parser: The argument parser to add arguments to
        """
        parser.add_argument(
            "--wallbox-host", help="Wallbox host URL", default=cls.wallbox_host
        )
        parser.add_argument(
            "--power-tag",
            help="Tag in MQTT data containing power information",
            default=cls.power_tag,
        )
        parser.add_argument(
            "--in-field",
            help="Field name in MQTT data containing energy input",
            default=cls.in_field,
        )
        parser.add_argument(
            "--out-field",
            help="Field name in MQTT data containing energy output",
            default=cls.out_field,
        )
        parser.add_argument(
            "--time-field",
            help="Field name in MQTT data containing timestamp",
            default=cls.time_field,
        )
        parser.add_argument(
            "--meter-id", type=int, help="Meter ID to use", default=cls.meter_id
        )

    @classmethod
    def ofYaml(cls, yaml_path):
        config = cls.load_from_yaml_file(yaml_path)
        return config

    def calcPower(self, payload) -> float:
        """
        Calculate power from payload using MeterReading class.

        Args:
            payload: The decoded JSON payload from MQTT message

        Returns:
            float: Calculated power in watts
        """
        # Get the data from the payload
        data = payload.get(self.power_tag, {})

        # Extract values
        e_in = data.get(self.in_field)
        e_out = data.get(self.out_field)
        timestamp_str = payload.get(self.time_field)

        # Create current reading
        current = MeterReading(kWh_in=e_in, kWh_out=e_out, time_stamp=timestamp_str)

        # If we don't have a previous reading, store this one and return fallback power
        if not hasattr(self, "_last_reading"):
            power = None
        else:
            power = current.active_power(self._last_reading)
        # Update stored reading
        self._last_reading = current
        return power


class PowerMeter:
    """Active power meter for Warp3 Wallbox"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.warp3_api = None

    def setup_logging(self, debug=False):
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
        self.logger = logging.getLogger(__name__)

    def check_warp3_availability(self):
        """Check Warp3 version and meter config"""
        # Check version
        version_info = self.warp3_api.get_version()
        if not version_info:
            self.logger.error("❌ Cannot connect to Warp3 API")
            return False

        firmware = version_info.get("firmware", "unknown")
        self.logger.info(f"✅ Connected to Warp3 - Firmware version: {firmware}")

        # Check meter
        meter_id = self.wallbox_config.meter_id
        meter_config = self.warp3_api.get_meter_config(meter_id)
        if not meter_config:
            self.logger.error(f"❌ Meter {meter_id} not available")
            return False

        self.logger.info(f"✅ Meter {meter_id} configured successfully")
        return True

    def handle_message(self, msg):
        """Handle incoming MQTT message"""
        try:
            payload = json.loads(msg.payload.decode())
            active_power = self.wallbox_config.calcPower(payload)
            if active_power:
                self.update_wallbox(active_power)
        except json.JSONDecodeError as jde:
            self.logger.error(f"JSON decode error: {str(jde)}")
        except Exception as e:
            self.logger.error(f"Error handling message: {str(e)}")

    def update_wallbox(self, power_value):
        """Send power value to wallbox"""
        self.logger.info(f"Power value: {power_value}W")

        if not self.mqtt_config.dry_run:
            self.warp3_api.update_meter(power_value, self.wallbox_config.meter_id)
        else:
            self.logger.info(f"DRY RUN: would update to {power_value}W")

    def start(self):
        """Start the power meter"""
        # Set up logging
        self.setup_logging(self.args.debug)

        # Initialize Warp3 API
        self.warp3_api = Warp3Api(self.wallbox_config.wallbox_host)

        # Log configuration
        self.logger.info("Starting MQTT to Warp3 middleware")
        self.logger.info(f"MQTT broker: {self.mqtt_config.mqtt_broker}")
        self.logger.info(f"MQTT topic: {self.mqtt_config.mqtt_topic}")
        self.logger.info(f"Wallbox host: {self.wallbox_config.wallbox_host}")
        self.logger.info(f"Power tag: {self.wallbox_config.power_tag}")
        self.logger.info(f"Meter ID: {self.wallbox_config.meter_id}")

        # Check API availability
        if not self.check_warp3_availability():
            self.logger.error("Cannot connect to Warp3 - exiting")
            sys.exit(1)

        # Create and run client
        client = MqttClient(self.mqtt_config, callback=self.handle_message)
        client.run()

    def maininstance(self):
        """Main instance setup and execution"""
        # Parse arguments
        self.parser = argparse.ArgumentParser(
            description="MQTT to Warp3 Wallbox Middleware"
        )
        self.parser.add_argument(
            "--config-path", help="Path to YAML configuration file"
        )
        MqttConfig.addArgs(self.parser)
        WallboxConfig.addArgs(self.parser)
        self.parser.add_argument(
            "--debug", action="store_true", help="Enable debug logging"
        )
        self.args = self.parser.parse_args()

        # Create configurations
        if self.args.config_path:
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Loading configuration from {self.args.config_path}")
            try:
                self.mqtt_config = MqttConfig.ofYaml(self.args.config_path)
                self.wallbox_config = WallboxConfig.ofYaml(self.args.config_path)
            except Exception as e:
                self.logger.error(f"Failed to load configuration from YAML: {e}")
                sys.exit(1)
        else:
            self.mqtt_config = MqttConfig.ofArgs(self.args)
            self.wallbox_config = WallboxConfig.ofArgs(self.args)

        self.start()


def main():
    """Main entry point"""
    pm = PowerMeter()
    pm.maininstance()


if __name__ == "__main__":
    main()
