from bluepy import btle
import gpiod
import time
import struct

# Set up GPIO for Buzzer using gpiod
BUZZER_PIN = 17
chip = gpiod.Chip("gpiochip0")
line = chip.get_line(BUZZER_PIN)
line.request(consumer="buzzer", type=gpiod.LINE_REQ_DIR_OUT)

# Bluetooth device MAC address
target_address = "E0:5A:1B:7A:1C:0E"

# Connect to the Bluetooth device and monitor distance
device = None
try:
    device = btle.Peripheral(target_address)
    print("Connected to Bluetooth device.")

    while True:
        data = device.readCharacteristic(12)
        
        if len(data) == 4:
            distance = struct.unpack('I', data)[0]
            print(f"Distance: {distance} cm")

            # Activate buzzer if distance is less than 20 cm
            if distance < 20:
                for _ in range(5):
                    line.set_value(1)
                    time.sleep(0.1)
                    line.set_value(0)
                    time.sleep(0.1)
            else:
                line.set_value(0)  # Ensure buzzer is off if distance is >= 20 cm

        time.sleep(0.5)

except btle.BTLEException as e:
    print(f"Bluetooth connection error: {e}")

finally:
    print("Releasing resources...")
    if device:
        device.disconnect()
    line.release()
