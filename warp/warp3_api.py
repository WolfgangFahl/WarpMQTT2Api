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
        self.meter_values={}

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

                prev=self.meter_values.get(meter_id)
                if not prev or prev!=value:
                    msg=f"✅ {value} Watt set for meter {meter_id}"
                    self.logger.info(msg)
                self.meter_values[meter_id]=value
                update_success = True
            else:
                self.logger.error(f"❌ Failed to update: {http_response.text}")
        except Exception as e:
            self.logger.error(f"Error updating meter: {e}")
        return update_success

    def describe_meter(self, meter: dict) -> str:
        """
        Describe the meter configuration using value_id explanations.

        Args:
            meter: The meter configuration dictionary.

        Returns:
            A human-readable description string.
        """
        name = meter.get('display_name', 'Unknown')
        location = meter.get('location', 'N/A')
        value_ids = meter.get('value_ids', [])
        values_explained = ', '.join(
            f"{vid}: {self.explain_value_id(vid)}" for vid in value_ids
        )
        description = f"Meter '{name}' at location {location} measures: {values_explained}"
        return description

    def explain_value_id(self,value_id: int) -> str:
        explanations = {
            1: "Spannung L1-N",
            2: "Spannung L2-N",
            3: "Spannung L3-N",
            4: "Spannung L1-L2",
            5: "Spannung L2-L3",
            6: "Spannung L3-L1",
            7: "Durchschnittliche Phasenspannung",
            8: "Durchschnitt Spannung L1-L2, L2-L3, L3-L1",
            13: "Strom (Bezug + Einspeisung)",
            17: "Strom (Bezug + Einspeisung)",
            21: "Strom (Bezug + Einspeisung)",
            25: "Neutralleiterstrom",
            29: "Durchschnitt der Phasenströme",
            33: "Summe der Phasenströme",
            39: "Wirkleistung (Bezug - Einspeisung)",
            48: "Wirkleistung (Bezug - Einspeisung)",
            57: "Wirkleistung (Bezug - Einspeisung)",
            74: "Summe der Phasenwirkleistungen (Bezug - Einspeisung)",
            83: "Blindleistung (induktiv - kapazitiv)",
            91: "Blindleistung (induktiv - kapazitiv)",
            99: "Blindleistung (induktiv - kapazitiv)",
            115: "Summe der Phasenblindleistungen",
            122: "Scheinleistung (Bezug + Einspeisung)",
            130: "Scheinleistung (Bezug + Einspeisung)",
            138: "Scheinleistung (Bezug + Einspeisung)",
            154: "Summe der Phasenscheinleistungen",
            209: "Wirkenergie Bezug (seit Herstellung)",
            210: "Wirkenergie Bezug (seit letztem Zurücksetzen)",
            211: "Wirkenergie Einspeisung (seit Herstellung)",
            212: "Wirkenergie Einspeisung (seit letztem Zurücksetzen)",
            213: "Wirkenergie Bezug + Einspeisung (seit Herstellung)",
            214: "Wirkenergie Bezug + Einspeisung (seit letztem Zurücksetzen)",
            277: "Blindenergie induktiv + kapazitiv (seit Herstellung)",
            353: "Leistungsfaktor (gerichtet)",
            354: "Leistungsfaktor (gerichtet)",
            355: "Leistungsfaktor (gerichtet)",
            356: "Summe der gerichteten Leistungsfaktoren",
            364: "Netzfrequenz",
        }
        return explanations.get(value_id, "Unknown value_id")

