# OctoPrint LattePanda Temperature Sensor Plugin 

This really basic plugin is based on [Vitor Henrique's Enclosure plugin](https://github.com/vitormhenrique/OctoPrint-Enclosure), but stripped down to just one task: get data over serial from a LattePanda's internal Arduno Leonardo about a set of one or more temperature sensors, then present those to OctoPrint.

Since the LattePanda does not have the convenient inbuilt GPIO of a Raspberry Pi, and also thus does not support the main Enclosure plugin this necessitated a different way to access the temperature sensors. I crafted up a small Arduino program to run on the Leonardo that would read the temperature sensors then output the readings every 2 seconds. This plugin then reads those over the `ttyAMA` serial interface, parses them, and presents them to OctoPrint.

Given the simplicity, I decided to use the "basic" plugin format. So simply edit `lattepandatemp.py` to suit your needs (specifically, for the serial settings if those differ for you), and put it into your OctoPrint `.octoprint/plugins/` directory.

To operate properly, you must make sure your OctoPrint user is in the `dialout` group (or whatever group has read perms on the relevant serial port).

This plugin requires the "Plotly Temp Graph" plugin to show the output in the main Temperature graphs.

# Arduino Sketch

The example Arduino sketch in `arduino.cpp` can be used on the Leonardo to output data from several AM2302 sensors in a format this plugin can handle. It requires the Adafruit DHT library for Arduino (available in the Arduino IDE plugin repository). Adjust the `SensorDatabase` array to customize for your own sensor configuration, or tweak the sketch to your liking (e.g. different sensor types).
