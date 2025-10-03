import machine
import network
import time
import urequests
import json
from machine import Pin

class DoorSensor:
    def __init__(self, sensor_pin=16, led_pin=25):
        self.sensor_pin = Pin(sensor_pin, Pin.IN, Pin.PULL_UP)
        self.led = Pin(led_pin, Pin.OUT)
        self.last_state = None
        self.debounce_time = 50
        self.last_trigger = 0

        # WiFi credentials - update these
        self.wifi_ssid = "YOUR_WIFI_SSID"
        self.wifi_password = "YOUR_WIFI_PASSWORD"

        # Optional webhook URL for notifications
        self.webhook_url = None

        self.wlan = None

    def connect_wifi(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

        if not self.wlan.isconnected():
            print(f"Connecting to WiFi: {self.wifi_ssid}")
            self.wlan.connect(self.wifi_ssid, self.wifi_password)

            timeout = 10
            while not self.wlan.isconnected() and timeout > 0:
                time.sleep(1)
                timeout -= 1
                print(".", end="")

            if self.wlan.isconnected():
                print(f"\nWiFi connected! IP: {self.wlan.ifconfig()[0]}")
                return True
            else:
                print("\nFailed to connect to WiFi")
                return False
        else:
            print(f"Already connected to WiFi. IP: {self.wlan.ifconfig()[0]}")
            return True

    def is_door_open(self):
        return self.sensor_pin.value() == 1

    def send_notification(self, door_state):
        if not self.webhook_url or not self.wlan or not self.wlan.isconnected():
            return

        try:
            data = {
                "door_state": "open" if door_state else "closed",
                "timestamp": time.time(),
                "device": "pico_w_door_sensor"
            }

            response = urequests.post(
                self.webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
            response.close()
            print(f"Notification sent: door {'open' if door_state else 'closed'}")
        except Exception as e:
            print(f"Failed to send notification: {e}")

    def flash_led(self, times=3):
        for _ in range(times):
            self.led.on()
            time.sleep(0.1)
            self.led.off()
            time.sleep(0.1)

    def run(self):
        print("Door sensor starting...")

        # Connect to WiFi
        if self.connect_wifi():
            self.flash_led(2)

        print("Monitoring door state. Press Ctrl+C to stop.")

        try:
            while True:
                current_time = time.ticks_ms()
                current_state = self.is_door_open()

                # Debounce the sensor reading
                if (self.last_state is None or
                    current_state != self.last_state and
                    time.ticks_diff(current_time, self.last_trigger) > self.debounce_time):

                    if current_state:
                        print("=ª Door OPENED")
                        self.led.on()
                    else:
                        print("=ª Door CLOSED")
                        self.led.off()

                    # Send notification if webhook is configured
                    self.send_notification(current_state)

                    self.last_state = current_state
                    self.last_trigger = current_time

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nStopping door sensor...")
            self.led.off()
            if self.wlan:
                self.wlan.disconnect()

# Configuration and usage
if __name__ == "__main__":
    # Create door sensor instance
    # Default: sensor on GPIO 16, LED on GPIO 25 (built-in LED)
    sensor = DoorSensor(sensor_pin=16, led_pin=25)

    # Configure WiFi credentials
    sensor.wifi_ssid = "YOUR_WIFI_SSID"
    sensor.wifi_password = "YOUR_WIFI_PASSWORD"

    # Optional: Configure webhook for notifications
    # sensor.webhook_url = "https://your-server.com/webhook"

    # Start monitoring
    sensor.run()