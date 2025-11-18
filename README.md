# autoyak

AutoYak is an open-source autopilot system for kayaks, powered by a Raspberry Pi Zero W. It uses a rotary encoder for steering input and a servo to control the rudder and motor, enabling hands-free navigation and course correction.

## Features

- Rotary encoder input for precise heading adjustment
- Servo control for rudder and motor actuation
- Compact, low-power Raspberry Pi Zero W onboard computer
- Modular design for different kayak setups

## Hardware Requirements

- Raspberry Pi Zero W
- Rotary encoder (for heading input)
- Servo motor (for rudder and/or throttle)
- Power supply (battery pack recommended)
- Kayak with rudder and/or motor

## Software Overview

- Python-based control logic
- Reads rotary encoder for desired heading
- Drives servo to adjust rudder/motor position
- Optional: GPS integration for waypoint navigation

## Getting Started

1. Assemble hardware according to your kayak’s configuration.
2. Connect rotary encoder and servo to Pi Zero W GPIO pins.
3. Clone this repository:
   ```sh
   git clone https://github.com/zodiac1214/autoyak.git
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Run the autopilot script:
   ```sh
   python autopilot.py
   ```

## Contributing

Pull requests and suggestions are welcome!

## License

MIT License
