"""
Created on 09.05.2025

@author: wf
"""

from argparse import Namespace
from typing import Optional

from lodstorage.yamlable import lod_storable


@lod_storable
class MqttConfig:
    """Configuration for the MQTT to Warp3 middleware"""

    mqtt_broker: str = "mqtt.bitplan.com"
    mqtt_port: int = 1883
    mqtt_topic: str = "tele/data"
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    dry_run: bool = False

    @classmethod
    def ofArgs(cls, args: Namespace = None):
        """
        Create a configuration from command line arguments.

        Args:
            args: Optional list of command line arguments. If None, sys.argv is used.

        Returns:
            MqttConfig: Configuration object
        """
        if args is None:
            config = cls()
        else:
            config = cls(
                mqtt_broker=args.mqtt_broker,
                mqtt_port=args.mqtt_port,
                mqtt_topic=args.mqtt_topic,
                mqtt_username=args.mqtt_username,
                mqtt_password=args.mqtt_password,
                dry_run=args.dry_run,
            )
        return config

    @classmethod
    def addArgs(cls, parser):
        """
        Add command line arguments for MqttConfig to the given parser.

        Args:
            parser: The argument parser to add arguments to
        """
        parser.add_argument(
            "--mqtt-broker", help="MQTT broker address", default=cls.mqtt_broker
        )
        parser.add_argument(
            "--mqtt-port", type=int, help="MQTT broker port", default=cls.mqtt_port
        )
        parser.add_argument(
            "--mqtt-topic", help="MQTT topic to subscribe to", default=cls.mqtt_topic
        )
        parser.add_argument(
            "--mqtt-username", help="MQTT username", default=cls.mqtt_username
        )
        parser.add_argument(
            "--mqtt-password", help="MQTT password", default=cls.mqtt_password
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="Run without updating the wallbox"
        )

    @classmethod
    def ofYaml(cls, yaml_path):
        config = cls.load_from_yaml_file(yaml_path)
        return config
