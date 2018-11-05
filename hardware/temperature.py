from database.admin import DataBase
from system.timer import TimerEvent
from w1thermsensor import W1ThermSensor

class TemperatureSensor():

    def __init__(self):
        self.update_seconds = 5
        self.h_temperature = 'h_temperature'

        self.read_sensor_timer = TimerEvent(self.update_seconds, self.read_sensor)
        self.read_sensor_timer.start()
        self.busy = False
    
    def is_busy(self):
        return self.busy

    def read_sensor(self):
        sensor = W1ThermSensor()
        self.busy = True
        
        try:
            temp = sensor.get_temperature()
            temp = '{0:.1f}'.format(temp)
            DataBase.set_value(self.h_temperature, temp)        
        except:
            print("Temperature Sensor reading failed.")
        
        self.busy = False

    def stop_timers(self):
        print("Stopping temperature sensor read event.")
        self.read_sensor_timer.cancel()
