"""
soft_pwm package.

This package provides software-based PWM control for RGB LEDs and other components using WiringPi.
"""

from .soft_pwm import SoftPWM, ToneGenerator, ServoController

__all__ = ['SoftPWM', 'ToneGenerator', 'ServoController']
