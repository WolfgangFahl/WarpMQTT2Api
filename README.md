# WarpMQTT2Api
Tinkerforge Warp MQTT 2 API bridge

[![pypi](https://img.shields.io/pypi/pyversions/WarpMQTT2Api)](https://pypi.org/project/WarpMQTT2Api/)
[![Github Actions Build](https://github.com/WolfgangFahl/WarpMQTT2Api/actions/workflows/build.yml/badge.svg)](https://github.com/WolfgangFahl/WarpMQTT2Api/actions/workflows/build.yml)
[![PyPI Status](https://img.shields.io/pypi/v/WarpMQTT2Api.svg)](https://pypi.python.org/pypi/WarpMQTT2Api/)
[![GitHub issues](https://img.shields.io/github/issues/WolfgangFahl/WarpMQTT2Api.svg)](https://github.com/WolfgangFahl/WarpMQTT2Api/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/WolfgangFahl/WarpMQTT2Api.svg)](https://github.com/WolfgangFahl/WarpMQTT2Api/issues/?q=is%3Aissue+is%3Aclosed)
[![API Docs](https://img.shields.io/badge/API-Documentation-blue)](https://WolfgangFahl.github.io/WarpMQTT2Api/)
[![License](https://img.shields.io/github/license/WolfgangFahl/WarpMQTT2Api.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Motivation
Tasmota based power meter sending MQTT messages such as:
```json
{"Time":"2025-05-10T08:24:13","eHZ":{"E_in":67299.845,"E_out":50268.783,"Power":0,"Power2":4111}}
```
see [Tasmota scripts](https://stromleser.de/blogs/scripts/ehm-zahler-tasmota-scripts-stromleser-wifi)

While the values can be send directly in the script e.g.
via:
```basj
=>WebQuery http://192.168.XXX.XXX/meters/1/update POST [Content-Type:application/json] [%sml[3]%]
```

there is still a problem with the sign of the power.

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
power_field: "Power2"
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
warp3 -h
usage: warp3 [-h] [--config-path CONFIG_PATH] [--mqtt-broker MQTT_BROKER]
             [--mqtt-port MQTT_PORT] [--mqtt-topic MQTT_TOPIC]
             [--mqtt-username MQTT_USERNAME] [--mqtt-password MQTT_PASSWORD]
             [--dry-run] [--wallbox-host WALLBOX_HOST] [--power-tag POWER_TAG]
             [--power-field POWER_FIELD] [--in-field IN_FIELD]
             [--out-field OUT_FIELD] [--time-field TIME_FIELD]
             [--meter-id METER_ID] [--update-interval UPDATE_INTERVAL]
             [--debug]

MQTT to Warp3 Wallbox Middleware

options:
  -h, --help            show this help message and exit
  --config-path CONFIG_PATH
                        Path to YAML configuration file
  --mqtt-broker MQTT_BROKER
                        MQTT broker address
  --mqtt-port MQTT_PORT
                        MQTT broker port
  --mqtt-topic MQTT_TOPIC
                        MQTT topic to subscribe to
  --mqtt-username MQTT_USERNAME
                        MQTT username
  --mqtt-password MQTT_PASSWORD
                        MQTT password
  --dry-run             Run without updating the wallbox
  --wallbox-host WALLBOX_HOST
                        Wallbox host URL
  --power-tag POWER_TAG
                        Tag in MQTT data containing power information
  --power-field POWER_FIELD
                        Field name in MQTT data containing active power value
  --in-field IN_FIELD   Field name in MQTT data containing energy input
  --out-field OUT_FIELD
                        Field name in MQTT data containing energy output
  --time-field TIME_FIELD
                        Field name in MQTT data containing timestamp
  --meter-id METER_ID   Meter ID to use
  --update-interval UPDATE_INTERVAL
                        Minimum update interval in seconds
  --debug               Enable debug logging

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
2025-05-09 16:33:33,312 - INFO - ✅ Meter 'Hausanschluss' at location 4 measures: 74: Summe der Phasenwirkleistungen (Bezug - Einspeisung)
2025-05-09 16:33:33,316 - INFO - Connected to MQTT broker at mqtt.bitplan.com
2025-05-09 16:33:33,316 - INFO - Subscribed to tele/tasmota_B13330/SENSOR
2025-05-09 16:33:43,423 - INFO - Power value: -360W
2025-05-09 16:33:43,433 - INFO - ✅ -360 Watt set
```

# Config on raspberry pi
```bash
## startup script
#!/bin/bash
# WF 2025-05-10
# Start Warp3 with nohup and log to /var/log/warp3

LOGDIR="/var/log/warp3"
LOGFILE="$LOGDIR/warp3.log"
APP="warp3"
OPTIONS="--config-path /home/wf/.warp3/config.yaml"

sudo mkdir -p "$LOGDIR"
sudo chmod 755 "$LOGDIR"
sudo chown wf:wf $LOGDIR

timestamp=$(date '+%F %T')
echo "$timestamp - INFO - 🚀 Starting warp3" >> "$LOGFILE"

nohup "$APP" $OPTIONS >> "$LOGFILE" 2>&1 &
```
## crontab entry
```bash
# run warp3 on reboot
@reboot /home/wf/bin/warp3start
```

## logrotate entry
```bash
cat /etc/logrotate.d/warp3
/var/log/warp3/warp3.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    delaycompress
    copytruncate
}
``



