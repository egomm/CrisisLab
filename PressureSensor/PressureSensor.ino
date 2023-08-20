#include <Wire.h>
#include "SparkFunBMP384.h"

// Create a new sensor object
BMP384 PressureSensor;

// I2C address selection
uint8_t i2cAddress = BMP384_I2C_ADDRESS_DEFAULT; // 0x77

void setup() {
    // Start serial
    Serial.begin(115200);

    // Initialize the I2C library
    Wire.begin();

    // Check if sensor is connected and initialize
    while (PressureSensor.beginI2C(i2cAddress) != BMP3_OK) {
        // Not connected, inform user
        Serial.println("Error: Pressure Sensor not Connected!");
        // Wait a bit to see if connection is established
        delay(1000);
    }
}

void loop() {
    // Get measurements from the sensor
    bmp3_data data = {0};
    int8_t err = PressureSensor.getSensorData(&data);

    // Check whether data was received successfully
    if (err == BMP3_OK) {
        Serial.println(data.pressure);
    }

    // Get pressure data every 250ms
    delay(250);
}
