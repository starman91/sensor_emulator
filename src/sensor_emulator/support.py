# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#		    		support.py
#
# A series of generic methods useful across the data harvest application
#              -------------------
# author 	      : Robert White
# date           : OCt 30, 2026
# copyright   : (C) 2026 by  NLR
# email         : robert.white@nlr.gov
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import json
import pandas as pd
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

#----------------------------------------------------------------------------------
def read_config_file(path_and_file):
    '''
    access and opens the configuration file for identifying sensor
    definitions, locations, operating ranges, and simulation parameters.
    All is processed into a dataframe.
    
    Parameters
    ----------------------
    path_and_file : string
         location and filename of the configuration file

    Returns
    ---------------------
    df_simulation : dataframe
         Simulation parameters including update interval and random seed

    df_locations : dataframe
         Location information including building, room, and zone

    df_sensors : dataframe
         Sensor definitions including operating ranges, noise,
         seasonal information, and spatial relationships
    '''
    with open(path_and_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
     
     # Extract simulation parameters
    df_simulation = pd.DataFrame([config.get('simulation', {})])

    # Extract location information
    df_locations = pd.DataFrame(config.get('locations', []))

    # Extract sensor definitions
    df_sensors = pd.DataFrame(config.get('sensors', []))

    print (f"All sensor, simulation, and location information extracted form config file {path_and_file}")
    return df_simulation, df_locations, df_sensors


# ---------------------------------------------------------------------------------------
def read_config_to_df (path_and_file):
    '''
    access and opens th configuration file for identifying target datbases,
    tables, and fields, along with format requiremnts of the field. All is processed
    into a dataframe.
  
    Parameters
    ----------------------
    path_and_file : string
         location and filename of the configuration file 
         
    Returns
    ---------------------
    df : dataframe
         Composite dataframe of the configuration Information
    '''
    try:
        df = pd.read_csv(path_and_file)
    except:
        print(f" problem opening file {path_and_file} into dataframe")
    else:
        print (f"File {path_and_file} opened into dataframe")
        
    print (df.info())
    return df

