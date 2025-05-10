"""
Created on 2025-09-05

@author: wf
"""
from argparse import Namespace
from tests.basetest import BaseTest
from warp.mqtt_config import MqttConfig  # adjust if module name differs


class TestMQTTConfig(BaseTest):
    """
    test the MqttConfig class
    """

    def setUp(self, debug=False, profile=True):
        super().setUp(debug, profile)

    def test_of_args(self):
        """
        test creating MqttConfig from argparse Namespace
        """
        args = Namespace(
            mqtt_broker="test.mqtt.com",
            mqtt_port=8883,
            mqtt_topic="test/topic",
            mqtt_username="user",
            mqtt_password="pass",
            dry_run=True
        )
        config = MqttConfig.ofArgs(args)
        self.assertEqual(config.mqtt_broker, "test.mqtt.com")
        self.assertEqual(config.mqtt_port, 8883)
        self.assertEqual(config.mqtt_topic, "test/topic")
        self.assertEqual(config.mqtt_username, "user")
        self.assertEqual(config.mqtt_password, "pass")
        self.assertTrue(config.dry_run)
