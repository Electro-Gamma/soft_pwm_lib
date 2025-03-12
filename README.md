# Soft PWM Library

This repository contains a Python library (`soft_pwm`) designed for software-based PWM control using WiringPi.  
It allows smooth control of RGB LEDs and other PWM-enabled components.

## Features

- **Software PWM Control**: Simulates hardware PWM using GPIO pins.
- **RGB LED Support**: Control Red, Green, and Blue channels independently.
- **Smooth Fading & Transitions**: Implements fade effects and color transitions.
- **Customizable Frequency & Duty Cycle**: Allows fine-tuned control.
- **Additional Support**: Includes tone generation and servo motor control.

## Requirements

- **Python 3.x**
- **WiringPi Library** (Ensure it is installed on your system)

## Installation

To install the package via pip (once uploaded to PyPI):

```bash
pip install soft_pwm
```

Or, clone this repository:

```bash
git clone https://github.com/Electro-Gamma/soft_pwm_lib.git
```

## Usage

1. Navigate to the project directory:
   ```bash
   cd soft_pwm_lib
   ```
2. Run the example script:
   ```bash
   python example/example.py
   ```

### Example Code

```python
from soft_pwm import SoftPWM

# Initialize the SoftPWM instance with RGB LED pins
pwm = SoftPWM(red_pin=2, green_pin=0, blue_pin=3)

# Set RGB color (Red)
pwm.set_rgb(255, 0, 0)

# Fade effect
pwm.fade(duration=0.02, steps=5)
```

## Configuration

You may need to adjust the GPIO pin numbers according to your hardware setup.

## Troubleshooting

If you encounter issues:

1. Ensure **WiringPi** is installed correctly on your system.
2. Run the script with proper permissions (`sudo` may be required on some systems).
3. Check the GPIO connections and verify pin numbers.

## Contributions

Contributions are welcome! Feel free to submit pull requests or open issues to suggest improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


