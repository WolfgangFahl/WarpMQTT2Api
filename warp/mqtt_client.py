"""
Created on 2025-05-09

@author: wf
"""

import logging

import paho.mqtt.client as mqtt
from warp.mqtt_config import MqttConfig

logger = logging.getLogger(__name__)


class MqttClient:
    """MQTT client"""

    def __init__(self, mqtt_config: MqttConfig, callback):
        """Initialize with configurations"""
        self.mqtt_config = mqtt_config
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.callback = callback

    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Connection callback"""
        if userdata or flags or properties:
            pass

        if rc == 0:
            logger.info(f"Connected to MQTT broker at {self.mqtt_config.mqtt_broker}")
            client.subscribe(self.mqtt_config.mqtt_topic)
            logger.info(f"Subscribed to {self.mqtt_config.mqtt_topic}")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        """Message callback"""
        if client or userdata:
            pass
        if isinstance(msg, mqtt.MQTTMessage):
            logger.debug(f"Message received: {msg.topic}")
            self.callback(msg)

    def run(self):
        """Run the client loop"""
        # Set up auth if needed
        if self.mqtt_config.mqtt_username and self.mqtt_config.mqtt_password:
            self.client.username_pw_set(
                self.mqtt_config.mqtt_username, self.mqtt_config.mqtt_password
            )

        # Connect to broker
        try:
            self.client.connect(
                self.mqtt_config.mqtt_broker, self.mqtt_config.mqtt_port
            )
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

        # Start loop
        try:
            logger.info("Starting MQTT loop")
            self.client.loop_forever()
        except KeyboardInterrupt:
            logger.info("Stopping client")
        except Exception as e:
            logger.error(f"Error in loop: {e}")
        finally:
            self.client.disconnect()

        return True
