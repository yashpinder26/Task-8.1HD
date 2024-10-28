#include <ArduinoBLE.h>

// Ultrasonic sensor pin configuration
const int trigPin = 11;
const int echoPin = 12;

// Variables for sensor reading
long duration;
int distance;

// BLE service and characteristic setup
BLEService distanceService("180D");  // Custom service UUID
BLEUnsignedIntCharacteristic distanceCharacteristic("2A37", BLERead | BLENotify);

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Configure sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Set up BLE
  if (!BLE.begin()) {
    Serial.println("Failed to initialize BLE!");
    while (1);  // Halt if BLE setup fails
  }

  // Configure BLE with service and characteristic
  BLE.setLocalName("ParkingSensor");
  BLE.setAdvertisedService(distanceService);
  distanceService.addCharacteristic(distanceCharacteristic);
  BLE.addService(distanceService);
  BLE.advertise();
}

void loop() {
  BLEDevice central = BLE.central();
  
  // Check for a connection
  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());

    while (central.connected()) {
      // Trigger the ultrasonic sensor
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);

      // Measure response duration and calculate distance
      duration = pulseIn(echoPin, HIGH);
      distance = duration * 0.034 / 2;

      // Log distance and update BLE characteristic
      Serial.print("Distance: ");
      Serial.print(distance);
      Serial.println(" cm");
      distanceCharacteristic.writeValue(distance);

      delay(1000);  // Wait before next reading
    }
    
    Serial.print("Disconnected from: ");
    Serial.println(central.address());
  }
}
