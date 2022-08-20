#include "DHT.h"

#define BAUDRATE 9600

struct Sensor {
  String  label;  // The label of the sensor, used to differentiate output values
  DHT     sensor; // The DHT sensor object; arguments of DIGITAL_PIN (e.g. "4") and SENSOR_TYPE (e.g. "DHT22" from DHT library)
};

Sensor SensorDatabase[] = {
  (Sensor) {
    "encl. upper", DHT(4, DHT22)
  },
  (Sensor) {
    "encl. lower", DHT(5, DHT22)
  }
};

const int SensorCount = sizeof(SensorDatabase) / sizeof(SensorDatabase[0]);

void setup() {
  Serial.begin(BAUDRATE); 

  for (int s = 0; s < SensorCount; s++) {
    SensorDatabase[s].sensor.begin();
  }
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  String output;
  for (int s = 0; s < SensorCount; s++) {
    float t = SensorDatabase[s].sensor.readTemperature();
    float h = SensorDatabase[s].sensor.readHumidity();

    output += SensorDatabase[s].label;
    output += ',';
    output += t;
    output += ',';
    output += h;

    if (s != SensorCount - 1) {
      output += '|';
    }
  }
  Serial.println(output);
}
