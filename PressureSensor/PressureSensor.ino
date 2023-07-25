#include <Wire.h>
#include "SparkFunBMP384.h"

// Create a new sensor object
BMP384 PressureSensor;

// I2C address selection
uint8_t i2cAddress = BMP384_I2C_ADDRESS_DEFAULT; // 0x77

void setup() {
    // Start serial
    Serial.begin(115200);
    Serial.println("BMP384 Begins!"); 

    // Initialize the I2C library
    Wire.begin();

    // Check if sensor is connected and initialize
    // Address is optional (defaults to 0x77)
    while (PressureSensor.beginI2C(i2cAddress) != BMP3_OK) {
        // Not connected, inform user
        Serial.println("Error: BMP384 not connected, check wiring and I2C address!");
        // Wait a bit to see if connection is established
        delay(1000);
    }
}

void loop() {
    // Get measurements from the sensor
    bmp3_data data = {0};
    int8_t err = PressureSensor.getSensorData(&data);

    // Check whether data was acquired successfully
    if (err == BMP3_OK) {
        /* Acquisistion succeeded, print temperature and pressure
        Serial.print("Temperature (C): ");
        Serial.print(data.temperature);
        */
        Serial.println(data.pressure);
    } else {
        // Acquisition failed, most likely a communication error (code -2)
        Serial.println("Error getting data from sensor! Error code: ");
        Serial.println(err);
    }

    delay(1000);
}
