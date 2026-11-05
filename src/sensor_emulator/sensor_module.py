# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#		    		sensor_module.py
#
# Manages a collection of simulated sensors.
#              -------------------
# author 	      : Robert White
# date           : Nov 5, 2026
# copyright   : (C) 2026 by  NLR
# email         : robert.white@nlr.gov
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

from sensor import Sensor


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
class SensorModule:
    '''
    Manages a collection of simulated sensors.
    '''

    def __init__(self, df_sensors, random_seed=None):
        '''
        Initialize sensors from the configuration dataframe.

        Parameters
        ----------------------
        df_sensors : dataframe
             Sensor configuration records

        random_seed : int or None
             Base random seed for sensor initialization
        '''
        self.sensors = {}

        for _, row in df_sensors.iterrows():
            sensor_config = row.to_dict()

            sensor = Sensor(config=sensor_config,random_seed=random_seed)
            self.sensors[sensor.sensor_id] = sensor
        return


    #----------------------------------------------------------------------------------
    def get_sensor(self, sensor_id):
        '''
        Return a sensor by its identifier.

        Parameters
        ----------------------
        sensor_id : str
             Unique sensor identifier

        Returns
        ---------------------
        sensor : Sensor
             Requested sensor instance
        '''
        return self.sensors[sensor_id]

    #----------------------------------------------------------------------------------
    def generate_readings(self):
        '''
        Generate one reading from every sensor.

        Returns
        ---------------------
        readings : list
             Reading records for all sensors
        '''
        readings = []

        for sensor in self.sensors.values():
            readings.append({
                'sensor_id': sensor.sensor_id,
                'location_id': sensor.location_id,
                'sensor_type': sensor.sensor_type,
                'value': sensor.update(),
                'unit': sensor.unit
            })

        return readings