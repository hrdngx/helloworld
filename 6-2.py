import time
from ADCDevice import *
import RPi.GPIO as GPIO

adc = ADCDevice()
LED_PIN = 18  # Define the pin for the LED

def setup():
    global adc

    if(adc.detectI2C(0x48)):
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)):
        adc = ADS7830()
    else:
        print("No correct ADC found,\n"
        "Please use command 'i2cdetect -y 1' to check I2C address! \n"
        "Program Exit. \n")
        exit(-1)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    global pwm
    pwm = GPIO.PWM(LED_PIN, 1000)  # Set PWM frequency to 1kHz
    pwm.start(0)  # Start PWM with 0% duty cycle

def loop():
    while True:
        value = adc.analogRead(0)
        voltage = value / 255.0 * 3.3
        duty_cycle = value / 255.0 * 100  # Convert value to duty cycle (0-100%)
        pwm.ChangeDutyCycle(duty_cycle)
        print('ADC Value: %d, Voltage: %.2f, Duty Cycle: %.2f' % (value, voltage, duty_cycle))
        time.sleep(0.1)

def destroy():
    adc.close()
    pwm.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    print('Program is starting')
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()