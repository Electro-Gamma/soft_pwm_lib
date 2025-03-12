import wiringpi as wp
import time
from softpwm import SoftPWM

# Set up GPIO pins for RGB and additional LED
RED_PIN = 2
GREEN_PIN = 0
BLUE_PIN = 3
PWM_LED = 29


# Choose "anode" or "cathode" based on your LED type
LED_TYPE = "anode"

# Create an instance of the SoftPWM class
driver = SoftPWM(red_pin=RED_PIN, green_pin=GREEN_PIN, blue_pin=BLUE_PIN, led_type=LED_TYPE)
driver2 = SoftPWM(pwm_led=PWM_LED)

try:

    # Example 1: Simple Fade from Off to Full Brightness
    print("Running Example 1: Simple fade from off to full brightness")
    driver.fade_rgb(from_red=0, from_green=0, from_blue=0, to_red=255, to_green=255, to_blue=255, steps=100, delay=0.01)

    # Example 2: Smooth Color Transition (Red to Green to Blue)
    print("Running Example 2: Smooth color transition from red to green to blue")
    driver.fade_rgb(from_red=255, from_green=0, from_blue=0, to_red=0, to_green=255, to_blue=0, steps=100, delay=0.01)
    driver.fade_rgb(from_red=0, from_green=255, from_blue=0, to_red=0, to_green=0, to_blue=255, steps=100, delay=0.01)
    driver.fade_rgb(from_red=0, from_green=0, from_blue=255, to_red=255, to_green=0, to_blue=0, steps=100, delay=0.01)

    # Example 3: Random Color Transitions for a Set Time
    print("Running Example 3: Random color transitions for 10 seconds")
    for _ in range(10):
        driver.set_random_color()
        time.sleep(1)
    
    # Example 4: Pulse Effect
    print("Running Example 4: Pulse effect, fading in and out 5 times")
    for _ in range(5):  # Repeat the pulse effect 5 times
        driver.fade_rgb(from_red=0, from_green=0, from_blue=0, to_red=255, to_green=255, to_blue=255, steps=50, delay=0.02)
        driver.fade_rgb(from_red=255, from_green=255, from_blue=255, to_red=0, to_green=0, to_blue=0, steps=50, delay=0.02)

    # Example 5: Slow Color Fade Between Specific Colors
    print("Running Example 5: Slow fade from dim yellow to bright cyan")
    driver.fade_rgb(from_red=128, from_green=128, from_blue=0, to_red=0, to_green=255, to_blue=255, steps=200, delay=0.05)

    # Example 6: Strobe Effect
    print("Running Example 6: Strobe effect with rapid on-off flashing")
    for _ in range(20):  # Repeat the strobe effect 20 times
        driver.set_rgb(255, 255, 255)  # Full brightness (white)
        time.sleep(0.05)  # Short delay
        driver.set_rgb(0, 0, 0)  # Off
        time.sleep(0.05)  # Short delay
        
    # Example 7: Fade PWM_LED
    print("Running Example 7: Starting fade test on PWM_LED for 10 seconds")
    for _ in range(10):
        driver2.fade(duration=0.02)
        
    # Example 8: Fade PWM_LED
    print("Running Example 8: Starting fade test on PWM_LED for 10 seconds")
    print("Starting fade test on LED_PIN from 10 to 255 'Ramp up' and 'Ramp down'")
    for _ in range(10):
        for duty in range(10, 256, 5):  # Ramp up
            #print(f"Testing Duty Cycle (Ramp Up): {duty}/255")
            driver2.fade_duty_cycle = duty
            time.sleep(0.02)
        for duty in range(255, 9, -5):  # Ramp down
            #print(f"Testing Duty Cycle (Ramp Down): {duty}/255")
            driver2.fade_duty_cycle = duty
            time.sleep(0.02)        
    
    # Example 9: Turn Off LEDs After Effects
    print("Turning off LEDs after completing the effect")
    driver.set_rgb(0, 0, 0)  # Turns off all LEDs

except KeyboardInterrupt:
    print("Exiting...")
    # Turn off LEDs before exiting
    wp.digitalWrite(PWM_LED, wp.LOW)    
    wp.digitalWrite(RED_PIN, wp.HIGH if LED_TYPE == "anode" else wp.LOW)
    wp.digitalWrite(GREEN_PIN, wp.HIGH if LED_TYPE == "anode" else wp.LOW)
    wp.digitalWrite(BLUE_PIN, wp.HIGH if LED_TYPE == "anode" else wp.LOW)

    print("LEDs turned off safely.")



