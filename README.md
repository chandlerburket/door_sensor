# Raspberry Pi Pico W Door Sensor

A MicroPython-based door sensor that monitors door state and provides WiFi connectivity for remote notifications.

## Hardware Requirements

- Raspberry Pi Pico W
- Magnetic door sensor (reed switch) or any open/close sensor
- Resistor (10kΩ recommended) for pull-up if sensor doesn't have one
- Breadboard and jumper wires

## Wiring

1. Connect the door sensor to GPIO 16:
   - One wire to GPIO 16
   - Other wire to GND
   - If your sensor needs a pull-up resistor, connect 10kΩ between GPIO 16 and 3.3V

2. Built-in LED (GPIO 25) will indicate door state:
   - ON = Door Open
   - OFF = Door Closed

## Setup Instructions

### 1. Install MicroPython on Pico W
1. Download the latest MicroPython firmware for Pico W from micropython.org
2. Hold BOOTSEL button while connecting Pico W to computer
3. Copy the .uf2 file to the RPI-RP2 drive
4. Pico W will reboot with MicroPython

### 2. Upload Files
Copy these files to your Pico W using Thonny, ampy, or your preferred tool:
- `door_sensor.py` - Main sensor code
- `config.py` - Configuration file

### 3. Configure Settings
Edit `config.py` or modify the values directly in `door_sensor.py`:
- Set your WiFi credentials
- Adjust GPIO pins if needed
- Configure webhook URL for notifications (optional)

### 4. Run the Sensor
```python
import door_sensor
sensor = door_sensor.DoorSensor()
sensor.wifi_ssid = "YourWiFiName"
sensor.wifi_password = "YourWiFiPassword"
sensor.run()
```

Or run directly: `python door_sensor.py`

## Features

- **Door State Monitoring**: Detects open/close state changes
- **Debouncing**: Prevents false triggers from sensor noise
- **WiFi Connectivity**: Connects to your local network
- **Visual Indicator**: Built-in LED shows door state
- **Web Notifications**: Optional webhook support for remote alerts
- **Low Power**: Efficient polling with minimal power consumption

## Sensor Logic

- **Closed Door**: Sensor pin reads LOW (0) - LED OFF
- **Open Door**: Sensor pin reads HIGH (1) - LED ON

This assumes a "normally closed" reed switch that opens when the magnet moves away.

## Webhook Notifications

If you configure a webhook URL, the sensor will send JSON POST requests:

```json
{
    "door_state": "open",
    "timestamp": 1234567890,
    "device": "pico_w_door_sensor"
}
```

## Troubleshooting

- **WiFi won't connect**: Check SSID/password, ensure 2.4GHz network
- **False triggers**: Increase debounce time or check wiring
- **No sensor readings**: Verify GPIO pin connections and pull-up resistor
- **Webhook fails**: Check URL and network connectivity

## Power Options

- USB power (5V)
- Battery pack (3.3V-5V)
- For battery operation, consider deep sleep modes between readings