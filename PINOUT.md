# Raspberry Pi Pico W Pinout for Door Sensor

## Pin Connections

```
                    Raspberry Pi Pico W

                    ┌─────────────────┐
                    │     USB Port    │
                    └─────────────────┘

    GP0  [ 1]  ●                 ● [40]  VBUS (5V)
    GP1  [ 2]  ●                 ● [39]  VSYS
    GND  [ 3]  ●                 ● [38]  GND
    GP2  [ 4]  ●                 ● [37]  3V3_EN
    GP3  [ 5]  ●                 ● [36]  3V3(OUT) ◄── For pull-up (optional)
    GP4  [ 6]  ●                 ● [35]  ADC_VREF
    GP5  [ 7]  ●                 ● [34]  GP28
    GND  [ 8]  ●                 ● [33]  GND (AGND)
    GP6  [ 9]  ●                 ● [32]  GP27
    GP7  [10]  ●                 ● [31]  GP26
    GP8  [11]  ●                 ● [30]  RUN
    GP9  [12]  ●                 ● [29]  GP22
    GND  [13]  ●  ◄── GND        ● [28]  GND
    GP10 [14]  ●                 ● [27]  GP21
    GP11 [15]  ●                 ● [26]  GP20
    GP12 [16]  ●                 ● [25]  GP19
    GP13 [17]  ●                 ● [24]  GP18
    GND  [18]  ●  ◄── GND        ● [23]  GND
    GP14 [19]  ●                 ● [22]  GP17
    GP15 [20]  ●                 ● [21]  GP16 ◄── Door Sensor Signal

                    └─────────────────┘
```

## Door Sensor Wiring

### Components Needed:
- Magnetic door sensor (reed switch)
- Jumper wires
- Optional: 10kΩ resistor (if sensor doesn't have built-in pull-up)

### Connection Diagram:

```
Door Sensor (Reed Switch)
    │
    │  Wire 1 ──────────────► GP16 (Pin 21) - Sensor Input
    │
    │  Wire 2 ──────────────► GND (Pin 13, 18, 23, or 28)
    │
```

### With External Pull-up Resistor (if needed):

```
    3V3 (Pin 36)
      │
      ├───[ 10kΩ ]─── GP16 (Pin 21)
      │                   │
                      Door Sensor
                          │
                        GND (Pin 13)
```

## Pin Assignments (from config.py)

| Function | GPIO Pin | Physical Pin | Notes |
|----------|----------|--------------|-------|
| Door Sensor Input | GP16 | Pin 21 | Reads door state (HIGH=open, LOW=closed) |
| Status LED | GP25 | Internal | Built-in LED on Pico W (WiFi LED) |
| Ground | GND | Pin 13, 18, 23, or 28 | Any GND pin works |
| Power (optional) | 3V3 | Pin 36 | For pull-up resistor |

## LED Behavior

The **built-in LED (GP25)** indicates door status:
- **LED ON** = Door is OPEN
- **LED OFF** = Door is CLOSED

The built-in LED will also flash during WiFi connection:
- **2 quick flashes** = WiFi connected successfully

## Sensor Logic

The code uses **PULL_UP** mode, which means:
- When the reed switch is **closed** (door closed, magnet near): Pin reads **LOW (0)** → Door CLOSED
- When the reed switch is **open** (door open, magnet away): Pin reads **HIGH (1)** → Door OPEN

## Typical Reed Switch Wiring

Most magnetic door sensors have two wires:
1. **Brown/Red wire** → GP16 (Pin 21)
2. **Blue/Black wire** → GND (Pin 13, 18, 23, or 28)

The Pico's internal pull-up resistor keeps the pin HIGH when the switch is open, and the pin goes LOW when the switch closes.

## Power Options

You can power the Pico W in several ways:
- **USB Cable** (recommended for testing) → VBUS pin
- **External 5V supply** → VSYS (Pin 39)
- **3.3V regulated supply** → 3V3(OUT) (Pin 36) - NOT recommended for powering, this is an output
- **Battery pack (3.7V-5V)** → VSYS (Pin 39) with appropriate regulation

## Quick Reference Photo Position

```
Looking at the Pico W with USB port at the TOP:

    USB PORT (Top)

Left Side:              Right Side:
GP0-GP15               GP16-GP28 ◄── Door Sensor here (GP16)
Multiple GND pins      Multiple GND pins ◄── Ground here

    Bottom
```

## Testing Your Connection

Once connected, you should see in the MicroPython console:
```
Connecting to WiFi: YourNetwork
....
WiFi connected! IP: 192.168.1.XXX
Monitoring door state. Press Ctrl+C to stop.
🚪 Door CLOSED  (or OPENED based on initial state)
```

When you open/close the door:
```
🚪 Door OPENED
🚪 Door CLOSED
```
