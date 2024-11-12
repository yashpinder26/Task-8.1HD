from bluepy import btle  # Import library to handle Bluetooth Low Energy (BLE) communication
import gpiod  # Import gpiod library to control GPIO pins on a Linux-based system
import time  # Import time library for adding delays
import struct  # Import struct library for unpacking binary data

# Set up GPIO for Buzzer using gpiod
BUZZER_PIN = 17  # GPIO pin number where the buzzer is connected
chip = gpiod.Chip("gpiochip0")  # Access the GPIO chip (gpiochip0 represents GPIO pins on the board)
line = chip.get_line(BUZZER_PIN)  # Get the line for the specific buzzer pin
line.request(consumer="buzzer", type=gpiod.LINE_REQ_DIR_OUT)  # Set pin as output for controlling the buzzer

# Bluetooth device MAC address (replace with the actual MAC address of the target device)
target_address = "E0:5A:1B:7A:1C:0E"

# Connect to the Bluetooth device and monitor distance readings
device = None  # Initialize device variable
try:
    # Try to connect to the Bluetooth device
    device = btle.Peripheral(target_address)
    print("Connected to Bluetooth device.")

    while True:
        # Read data from characteristic at handle 12 (replace with the correct handle if different)
        data = device.readCharacteristic(12)
        
        # Check if the data received is 4 bytes, representing an integer distance value
        if len(data) == 4:
            # Unpack the 4-byte data into an integer
            distance = struct.unpack('I', data)[0]
            print(f"Distance: {distance} cm")

            # If the distance is less than 20 cm, activate the buzzer as a warning
            if distance < 20:
                for _ in range(5):  # Beep the buzzer 5 times
                    line.set_value(1)  # Turn on buzzer
                    time.sleep(0.1)  # Wait for 0.1 seconds
                    line.set_value(0)  # Turn off buzzer
                    time.sleep(0.1)  # Wait for 0.1 seconds
            else:
                line.set_value(0)  # Ensure buzzer is off if distance is >= 20 cm

        # Wait before reading the distance again
        time.sleep(0.5)

# Handle Bluetooth connection errors
except btle.BTLEException as e:
    print(f"Bluetooth connection error: {e}")

# Ensure resources are released properly, whether or not an error occurs
finally:
    print("Releasing resources...")
    if device:
        device.disconnect()  # Disconnect the Bluetooth device if connected
    line.release()  # Release the GPIO line for the buzzer
