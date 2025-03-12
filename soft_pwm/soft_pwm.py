import wiringpi as wp
import time
import threading
import random

# Set up GPIO pins for RGB and additional LED
RED_PIN = 0
GREEN_PIN = 2
BLUE_PIN = 3
PWM_LED = 29

# PWM frequency and period
PWM_FREQUENCY = 1000  # 1 kHz for smoother colors
PWM_PERIOD = 1.0 / PWM_FREQUENCY

class SoftPWM:
    def __init__(self, red_pin=None, green_pin=None, blue_pin=None, pwm_led=None):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.pwm_led = pwm_led

        # Set up GPIO if pins are provided
        wp.wiringPiSetup()
        if self.red_pin is not None:
            wp.pinMode(self.red_pin, wp.OUTPUT)
        if self.green_pin is not None:
            wp.pinMode(self.green_pin, wp.OUTPUT)
        if self.blue_pin is not None:
            wp.pinMode(self.blue_pin, wp.OUTPUT)
        if self.pwm_led is not None:
            wp.pinMode(self.pwm_led, wp.OUTPUT)

        # Initialize current RGB values and fade duty cycle
        self.current_rgb = {'R': 0, 'G': 0, 'B': 0}
        self.fade_duty_cycle = 0

        # Lock for thread-safe access to shared variables
        self.lock = threading.Lock()

        # Start PWM threads only for the provided pins
        if self.red_pin is not None:
            threading.Thread(target=self.soft_pwm, args=(self.red_pin,), daemon=True).start()
        if self.green_pin is not None:
            threading.Thread(target=self.soft_pwm, args=(self.green_pin,), daemon=True).start()
        if self.blue_pin is not None:
            threading.Thread(target=self.soft_pwm, args=(self.blue_pin,), daemon=True).start()
        if self.pwm_led is not None:
            threading.Thread(target=self.soft_pwm, args=(self.pwm_led,), daemon=True).start()

    def soft_pwm(self, pin):
        """ PWM control for a given pin, using the current RGB values or fade duty cycle. """
        while True:
            with self.lock:
                # Get the current duty cycle for the pin
                if pin == self.red_pin:
                    duty_cycle = self.current_rgb['R']
                elif pin == self.green_pin:
                    duty_cycle = self.current_rgb['G']
                elif pin == self.blue_pin:
                    duty_cycle = self.current_rgb['B']
                elif pin == self.pwm_led:
                    duty_cycle = self.fade_duty_cycle
                else:
                    duty_cycle = 0  # Default to 0 if the pin is not RGB or LED

            # Set the pin low directly if duty cycle is 0
            if duty_cycle == 0:
                wp.digitalWrite(pin, wp.LOW)
                time.sleep(PWM_PERIOD)  # Avoid busy-waiting
                continue

            # Calculate on/off times based on duty cycle
            on_time = PWM_PERIOD * (duty_cycle / 255.0)
            off_time = PWM_PERIOD - on_time

            # Control the LED
            wp.digitalWrite(pin, wp.HIGH)
            time.sleep(on_time)
            wp.digitalWrite(pin, wp.LOW)
            time.sleep(off_time)

    def fade(self, duration=0.02, steps=5):
        """ Ramp up and down the LED connected to pwm_led only. """
        if self.pwm_led is not None:
            for duty in range(0, 256, steps):  # Ramp up
                with self.lock:
                    self.fade_duty_cycle = duty
                time.sleep(duration)
            for duty in range(255, -1, -steps):  # Ramp down
                with self.lock:
                    self.fade_duty_cycle = duty
                time.sleep(duration)

    def set_rgb(self, r, g, b):
        """ Set the RGB LED colors, if RGB pins are initialized. """
        with self.lock:
            if self.red_pin is not None:
                self.current_rgb['R'] = r
            if self.green_pin is not None:
                self.current_rgb['G'] = g
            if self.blue_pin is not None:
                self.current_rgb['B'] = b
        print(f"Setting RGB to: R={r}, G={g}, B={b}")
        
class ToneGenerator:
    def __init__(self, pin):
        """
        Initialize the ToneGenerator with a specified GPIO pin.
        
        :param pin: The GPIO pin number to output the tone
        """
        self.pin = pin
        wp.wiringPiSetup()  # Initialize WiringPi
        wp.pinMode(self.pin, wp.OUTPUT)  # Set the pin to OUTPUT

    def tone(self, frequency, duration):
        """
        Simulate Arduino's tone() function.
        
        :param frequency: Frequency of the tone in Hz
        :param duration: Duration of the tone in milliseconds
        """
        period = 1.0 / frequency  # in seconds
        half_period = period / 2  # half period for high and low states
        cycles = int((duration / 1000.0) / period)  # Calculate cycles

        for _ in range(cycles):
            wp.digitalWrite(self.pin, wp.HIGH)  # Set pin HIGH
            time.sleep(half_period)  # Wait for half the period
            wp.digitalWrite(self.pin, wp.LOW)   # Set pin LOW
            time.sleep(half_period)  # Wait for half the period

    def no_tone(self):
        """ Stop generating tone on the pin. """
        wp.digitalWrite(self.pin, wp.LOW)  # Set pin LOW to stop the tone
        
        
class ServoController:
    def __init__(self, pin):
        self.pin = pin
        wp.wiringPiSetup()  # Initialize WiringPi
        wp.pinMode(self.pin, wp.OUTPUT)  # Set the pin to OUTPUT
        self.position = 0  # Initial position

    def write(self, angle):
        if 0 <= angle <= 180:
            # Map the angle to pulse width (1 ms to 2 ms for 0 to 180 degrees)
            pulse_width = 500 + (angle / 180.0) * 2000  # Pulse width in microseconds
            wp.digitalWrite(self.pin, wp.HIGH)  # Set pin HIGH
            time.sleep(pulse_width / 1000000.0)  # Convert microseconds to seconds
            wp.digitalWrite(self.pin, wp.LOW)  # Set pin LOW
            time.sleep(20 / 1000.0)  # Wait for 20 ms (servo control period)
            self.position = angle
        else:
            print("Angle must be between 0 and 180 degrees.")

    def read(self):
        return self.position


# Example usage:
# # Only PWM LED
# soft_pwm_controller= SoftPWM(pwm_led=29)
# 
# # Only RGB
# soft_pwm_controller = SoftPWM(red_pin=0, green_pin=2, blue_pin=3)

# Create an instance of the SoftPWM class
soft_pwm_controller = SoftPWM(red_pin=RED_PIN, green_pin=GREEN_PIN, blue_pin=BLUE_PIN, pwm_led=PWM_LED)

# Main loop to demonstrate fade effect
try:
    while True:
        # Set a random RGB color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        soft_pwm_controller.set_rgb(r, g, b)  # Set the RGB colors
        
        # Example fade effect
        fade_duration = 0.02  # Duration for each step
        fade_steps = 5        # Steps for fading
        print("Starting fade effect...")
        soft_pwm_controller.fade(duration=fade_duration, steps=fade_steps)

        # Additional ramp up and down for LED_PIN
        print("Starting fade test on LED_PIN...")
        for duty in range(0, 256, 5):  # Ramp up
            print(f"Testing Duty Cycle (Ramp Up): {duty}/255")
            soft_pwm_controller.fade_duty_cycle = duty
            time.sleep(0.02)
        
        for duty in range(255, -1, -5):  # Ramp down
            print(f"Testing Duty Cycle (Ramp Down): {duty}/255")
            soft_pwm_controller.fade_duty_cycle = duty
            time.sleep(0.02)

except KeyboardInterrupt:
    print("Exiting...")
    wp.digitalWrite(RED_PIN, wp.LOW)
    wp.digitalWrite(GREEN_PIN, wp.LOW)
    wp.digitalWrite(BLUE_PIN, wp.LOW)
    wp.digitalWrite(PWM_LED, wp.LOW)  # Turn off LED on exit

