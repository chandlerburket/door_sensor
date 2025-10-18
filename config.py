# Configuration file for Door Sensor
# Copy this file and update with your settings

# WiFi Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# Hardware Configuration
SENSOR_PIN = 16  # GPIO pin connected to door sensor
LED_PIN = 25     # GPIO pin for status LED (25 is built-in LED)

# Sensor Configuration
DEBOUNCE_TIME_MS = 50  # Milliseconds to debounce sensor readings

# Notification Configuration (optional)
WEBHOOK_URL = "http://192.168.1.100:5000/webhook"  # Security camera webhook URL
# Example: WEBHOOK_URL = "http://192.168.1.100:5000/webhook"

# Device Configuration
DEVICE_NAME = "pico_w_door_sensor"