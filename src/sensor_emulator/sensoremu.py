
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#		    		sensoremu.py
#
# This is the main file for creating a bank of emulated sensor traces to be used
# for testing hardware or digital twin system, when the live sensors are not 
# available
#              -------------------
# author 	      : Robert White
# date           : OCt 30, 2026
# copyright   : (C) 2026 by  NLR
# email         : robert.white@nlr.gov
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import argparse
import pandas as pd
import time

import support as sp
from sensor import Sensor
from sensor_module import SensorModule

df_simulation = pd.DataFrame()
df_locations = pd.DataFrame()
df_sensors = pd.DataFrame()

def main():
    print (f"Initializing operations")
    update_interval = df_simulation.loc[0, 'update_interval_seconds']
    random_seed = int(df_simulation.loc[0, 'random_seed'])  
    sensor_module = SensorModule(df_sensors=df_sensors,random_seed=random_seed)
   
    # Initialize sensors
    #sensors = {}
    #for _, row in df_sensors.iterrows():
        ##build each sensor, one at a time
        #sensor = Sensor(config=row.to_dict(),random_seed=random_seed)
        #sensors[sensor.sensor_id] = sensor
   
    while True:      
        #Get readings for sensors
        readings = sensor_module.generate_readings()
        #Display
        for reading in readings:
            print(reading)
        #Loop delay
        time.sleep(update_interval)  
   
    # Exit app
    quit
    

if __name__ == '__main__':

    print ('...:  Starting Sensor Emullator Program :...')
    # Get passed in args
    parser = argparse.ArgumentParser()
    
    #Argument setup 
    parser.add_argument('-f', nargs='?', type=str, help="SenEmu Operation Confuration File.")
    args = parser.parse_args()
    
    #Get sensor configurations
    df_simulation, df_locations, df_sensors = sp.read_config_file(args.f)  
    
    main()
