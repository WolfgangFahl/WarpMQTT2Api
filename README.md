# WarpMQTT2Api
Tinkerforge Warp MQTT 2 API bridge

[![pypi](https://img.shields.io/pypi/pyversions/WarpMQTT2Api)](https://pypi.org/project/WarpMQTT2Api/)
[![Github Actions Build](https://github.com/WolfgangFahl/WarpMQTT2Api/actions/workflows/build.yml/badge.svg)](https://github.com/WolfgangFahl/WarpMQTT2Api/actions/workflows/build.yml)
[![PyPI Status](https://img.shields.io/pypi/v/WarpMQTT2Api.svg)](https://pypi.python.org/pypi/WarpMQTT2Api/)
[![GitHub issues](https://img.shields.io/github/issues/WolfgangFahl/WarpMQTT2Api.svg)](https://github.com/WolfgangFahl/WarpMQTT2Api/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/WolfgangFahl/WarpMQTT2Api.svg)](https://github.com/WolfgangFahl/WarpMQTT2Api/issues/?q=is%3Aissue+is%3Aclosed)
[![API Docs](https://img.shields.io/badge/API-Documentation-blue)](https://WolfgangFahl.github.io/WarpMQTT2Api/)
[![License](https://img.shields.io/github/license/WolfgangFahl/WarpMQTT2Api.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Installation
```bash
git clone https://github.com/WolfgangFahl/WarpMQTT2Api
pip install .
```
## 🧪 Example Configuration

Store this as `~/.warp3/config.yaml`:

```yaml
# WF 2025-09-05
# warp3 middleware configs
# this is for a Tasmota device reading the energy meter

# Wallbox
wallbox_host: "http://wallbox" # replace with your wallbox address
power_tag: "eHZ"
in_field: "E_in"
out_field: "E_out"
time_field: "Time"
meter_id: 2

# MQTT
mqtt_broker: "mqtt.bitplan.com"
mqtt_port: 1883
mqtt_topic: "tele/tasmota_*****/SENSOR" # replace with your tasmota device
mqtt_username: "*****" # replace with your user
mqtt_password: "********"  # replace with your actual password
update_interval: 1  # every second
dry_run: false
```

# Command line usage
```bash
warp3 -h
```

```bash
usage: warp3 [-h] [--config-path CONFIG_PATH] [--mqtt-broker MQTT_BROKER]
             [--mqtt-port MQTT_PORT] [--mqtt-topic MQTT_TOPIC]
             [--mqtt-username MQTT_USERNAME] [--mqtt-password MQTT_PASSWORD]
             [--update-interval UPDATE_INTERVAL] [--dry-run]
             [--wallbox-host WALLBOX_HOST] [--power-tag POWER_TAG]
             [--in-field IN_FIELD] [--out-field OUT_FIELD]
             [--time-field TIME_FIELD] [--meter-id METER_ID] [--debug]

```

# Example output
```bash
warp3 --config-path $HOME/.warp3/config.yaml
2025-05-09 16:33:33,286 - INFO - Starting MQTT to Warp3 middleware
2025-05-09 16:33:33,286 - INFO - MQTT broker: mqtt.bitplan.com
2025-05-09 16:33:33,286 - INFO - MQTT topic: tele/tasmota_B13330/SENSOR
2025-05-09 16:33:33,286 - INFO - Wallbox host: http://wallbox.bitplan.com
2025-05-09 16:33:33,286 - INFO - Power tag: eHZ
2025-05-09 16:33:33,286 - INFO - Meter ID: 2
2025-05-09 16:33:33,303 - INFO - ✅ Connected to Warp3 - Firmware version: 2.8.0+6810d7c9
2025-05-09 16:33:33,312 - INFO - ✅ Meter 2 configured successfully
2025-05-09 16:33:33,315 - INFO - Starting MQTT loop
2025-05-09 16:33:33,316 - INFO - Connected to MQTT broker at mqtt.bitplan.com
2025-05-09 16:33:33,316 - INFO - Subscribed to tele/tasmota_B13330/SENSOR
2025-05-09 16:33:43,423 - INFO - Power value: -360W
2025-05-09 16:33:43,433 - INFO - ✅ -360 Watt set
```


