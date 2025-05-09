"""
Created on 2025-05-09

@author: wf
"""

import logging

import requests


class Warp3Api:
    """API client for TinkerForge/Warp3 Wallbox"""

    def __init__(self, host):
        """Initialize with wallbox host"""
        self.host = host.rstrip("/")
        self.logger = logging.getLogger(__name__)

    def api_get(self, cmd):
        """
        Call the wallbox API with the given command and filter the JSON result

        Args:
            cmd: API command


        Returns:
            API response
        """
        api_response = None
        try:
            http_response = requests.get(f"{self.host}/{cmd}")
            http_response.raise_for_status()
            api_response = http_response.json()
        except Exception as e:
            self.logger.error(f"API GET error: {e}")
        return api_response

    def get_version(self):
        """Get wallbox firmware version"""
        version_info = self.api_get("info/version")
        return version_info

    def get_meter_config(self, meter_id=1):
        """Get meter configuration"""
        meter_config = self.api_get(f"meters/{meter_id}/config")
        return meter_config

    def update_meter(self, value, meter_id=1):
        """
        Update meter value

        Args:
            value: Power value in Watts
            meter_id: Meter ID (default 1)

        Returns:
            True if successful, False otherwise
        """
        update_success = False
        try:
            url = f"{self.host}/meters/{meter_id}/update"
            http_response = requests.post(url, data=f"[{value}]")
            if http_response.status_code == 200 and not http_response.text:
                self.logger.info(f"✅ {value} Watt set")
                update_success = True
            else:
                self.logger.error(f"❌ Failed to update: {http_response.text}")
        except Exception as e:
            self.logger.error(f"Error updating meter: {e}")
        return update_success
