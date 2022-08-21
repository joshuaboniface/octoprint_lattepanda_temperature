# coding=utf-8
from __future__ import absolute_import
import serial
from octoprint.util import RepeatedTimer
import octoprint.plugin


# LattePanda Arduino Serial settings
serial_port = "/dev/ttyACM1"
serial_baud = 9600
serial_timeout = 5

# Specify the update interval in seconds; the actual time could be up to 2 seconds longer
# while waiting for the Arduino to print the next line
update_interval = 5


class LattePandaTemperaturePlugin(octoprint.plugin.StartupPlugin):
    temperature_sensor_data = []

    def __init__(self):
        pass

    def on_after_startup(self):
        self.start_timer()

    def start_timer(self):
        """
        Function to start time that checks the temperatures
        """

        self._check_temp_timer = RepeatedTimer(update_interval, self.check_temp, None, None, True)
        self._check_temp_timer.start()

    def check_temp(self):
        self._logger.debug("checking temperatures")
        
        try:
            ser = serial.Serial(
                port=serial_port,
                baudrate=serial_baud,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=serial_timeout)
            line = ser.readline().decode('ascii')
            ser.close()
        except Exception as e:
            self._logger.warn("failed to get temperatures: {}".format(e))
            line = ""

        if line:
            sensor_data = list()
            for sensor in line.split('|'):
                try:
                    label, temperature, humidity = sensor.strip().split(',')
                    self._logger.debug("sensor {}: {} *C, {} %RH".format(label, temperature, humidity))
                    sensor_data.append(dict(label=label, temperature=temperature, humidity=humidity, airquality=0))
                except ValueError as e:
                    self._logger.warn("failed to get temperatures: string: '{}' error: {}".format(sensor.strip(), e))
            self.temperature_sensor_data = sensor_data
            self.update_ui()
        
    def update_ui(self):
        self._plugin_manager.send_plugin_message(self._identifier, dict(sensor_data=self.temperature_sensor_data))

    def get_graph_data(self, comm, parsed_temps):
        for sensor in self.temperature_sensor_data:
            parsed_temps[str(sensor['label'])] = (sensor['temperature'], None)

        return parsed_temps


__plugin_name__ = "LattePanda Temperature Plugin"
__plugin_version__ = "0.0.1"
__plugin_description__ = "Show temerature sensor data from the LattePanda Arduino"
__plugin_pythoncompat__ = ">=3.6,<4"
__plugin_implementation__ = LattePandaTemperaturePlugin()
__plugin_hooks__ = {
    "octoprint.comm.protocol.temperatures.received": (__plugin_implementation__.get_graph_data, 1)
}
