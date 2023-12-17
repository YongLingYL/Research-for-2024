import smbus
import time

# Define I2C parameters
I2C_ADDR = 0x27  # I2C address of the LCD
I2C_BUS = 1  # Use bus 1 for Raspberry Pi 4

# Bit masks for data bits
En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001  # Register select bit

# Initialize I2C bus
bus = smbus.SMBus(I2C_BUS)

def lcd_init():
    # Initialize the display
    lcd_byte(0x03)
    lcd_byte(0x03)
    lcd_byte(0x03)
    lcd_byte(0x02)

    # Set the LCD function
    lcd_byte(0x20 | 0x08 | 0x04, 0)
    # Set the LCD display control
    lcd_byte(0x0C, 0)
    # Clear the display
    lcd_byte(0x01, 0)
    time.sleep(0.002)  # Wait for the clear command to complete
    # Set the entry mode
    lcd_byte(0x06, 0)

def lcd_byte(bits, mode=0):
    # Send byte to data pins
    bits_high = mode | (bits & 0xF0)
    bits_low = mode | ((bits << 4) & 0xF0)

    # High bits
    bus.write_byte(I2C_ADDR, bits_high | En)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low | En)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, bits & ~En)
    time.sleep(0.0005)

def lcd_string(message, line):
    # Send string to display
    message = message.ljust(16, " ")
    lcd_byte(line, Rs)
    for i in range(16):
        lcd_byte(ord(message[i]), Rs)

try:
    # Initialize the LCD
    lcd_init()

    while True:
        # Get input from the user
        num1 = input("Enter number 1: ")
        num2 = input("Enter number 2: ")

        # Display the two numbers on the LCD
        lcd_string(f"Num1: {num1}", 0x80)
        lcd_string(f"Num2: {num2}", 0xC0)

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    # Clear the display on exit
    lcd_byte(0x01, 0)
    time.sleep(0.002)
    # Close I2C bus
    bus.close()
