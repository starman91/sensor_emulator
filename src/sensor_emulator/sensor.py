# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#		    		sensor.py
#
# Class to create instances of sensors to be queired. Each instance will:
# Maintain its own sensor configuration.
# Store its current reading.
# Generate a new reading when update() is called.
# Keep readings within its configured limits.
# Allow its target, range, and noise to be changed dynamically.
# Support reproducible random behavior using a random seed.
#              -------------------
# author 	      : Robert White
# date           : OCt 30, 2026
# copyright   : (C) 2026 by  NLR
# email         : robert.white@nlr.gov
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import random
from abc import ABC, abstractmethod


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
class SensorBase(ABC):
    '''
    Base class defining the interface for an individual sensor.
    '''

    def __init__(self, config):
        '''
        Initialize common sensor configuration.

        Parameters
        ----------------------
        config : dict
             Configuration values for the sensor
        '''
        self.config = config

        self.sensor_id = config['sensor_id']
        self.sensor_type = config['sensor_type']
        self.location_id = config['location_id']
        self.unit = config['unit']

    @abstractmethod
    def update(self):
        '''
        Generate and return the sensor's next reading.

        Returns
        ---------------------
        value : float
             Updated sensor reading
        '''
        pass



#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
class Sensor(SensorBase):
    '''
    Simulated sensor representing an individual physical sensor.
    '''
    #--------------------------------------------------------------------------------
    def __init__(self, config, random_seed=None):
        '''
        initialize the sensor using its configuration.

        Parameters
        ----------------------
        config : dictionary
             sensor configuration from the configuration dataframe

        random_seed : integer
             optional seed for reproducible random behavior

        Returns
        ---------------------
        None
             initializes the sensor instance
        '''
        super().__init__(config)
        
        # Sensor identification
        self.sensor_id = config['sensor_id']
        self.sensor_type = config['sensor_type']
        self.location_id = config['location_id']
        self.unit = config['unit']

        # Operating parameters
        self.min_value = float(config['min_value'])
        self.max_value = float(config['max_value'])
        self.target_value = float(config['target_value'])
        self.noise_level = float(config['noise_level'])

        # Initial sensor reading
        self.initial_value = float(config['initial_value'])
        self.current_value = self.initial_value

        # Outdoor sensor information
        self.outdoor = config.get('outdoor', False)
        self.season = config.get('season', None)

        # Spatial relationships
        self.hadjacent = config.get('hadjacent', [])
        self.vhadjacent = config.get('vhadjacent', [])

        # Random number generator
        self.rng = random.Random(random_seed)

        # Sensor status
        self.status = 'normal'

        # Validate configuration
        self._validate_config()
        return

    #--------------------------------------------------------------------------------
    def _validate_config(self):
        '''
        validate the sensor configuration.

        Parameters
        ----------------------
        None

        Returns
        ---------------------
        None
             raises an exception if configuration is invalid
        '''

        if self.min_value >= self.max_value:
            raise ValueError(f'{self.sensor_id}: min_value must be less than max_value')

        if not self.min_value <= self.initial_value <= self.max_value:
            raise ValueError(f'{self.sensor_id}: initial_value outside operating range')

        if not self.min_value <= self.target_value <= self.max_value:
            raise ValueError(f'{self.sensor_id}: target_value outside operating range')

        if self.noise_level < 0:
            raise ValueError(f'{self.sensor_id}: noise_level cannot be negative')
        return

    #--------------------------------------------------------------------------------
    def update(self, alpha=0.1):
        '''
        generate the next sensor reading.

        Parameters
        ----------------------
        alpha : float
             rate at which the sensor moves toward its target value

        Returns
        ---------------------
        current_value : float
             updated sensor reading
        '''

        # Movement toward target
        target_change = alpha * (self.target_value - self.current_value)

        # Random disturbance
        noise = self.rng.gauss(0.0,self.noise_level)

        # Calculate new reading
        new_value = (self.current_value+ target_change+ noise)

        # Keep reading within operating limits
        self.current_value = max(self.min_value,min(self.max_value, new_value))

        return self.current_value


    #--------------------------------------------------------------------------------
    def set_target(self, target_value):
        '''
        change the sensor target value.

        Parameters
        ----------------------
        target_value : float
             new target operating value

        Returns
        ---------------------
        None
        '''

        self.target_value = float(target_value)
        return

    #--------------------------------------------------------------------------------
    def set_range(self, min_value, max_value):
        '''
        change the sensor operating range.

        Parameters
        ----------------------
        min_value : float
             new minimum operating value

        max_value : float
             new maximum operating value

        Returns
        ---------------------
        None
        '''

        if min_value >= max_value:
            raise ValueError(
                f'{self.sensor_id}: min_value must be less than max_value'
            )

        self.min_value = float(min_value)
        self.max_value = float(max_value)

        # Ensure current reading remains within range
        self.current_value = max(self.min_value,min(self.max_value, self.current_value))
        return

    #--------------------------------------------------------------------------------
    def set_noise(self, noise_level):
        '''
        change the sensor noise level.

        Parameters
        ----------------------
        noise_level : float
             standard deviation of random fluctuations

        Returns
        ---------------------
        None
        '''

        if noise_level < 0:
            raise ValueError(f'{self.sensor_id}: noise_level cannot be negative')
        self.noise_level = float(noise_level)
        return

    #--------------------------------------------------------------------------------
    def reset(self):
        '''
        reset the sensor to its initial reading.

        Parameters
        ----------------------
        None

        Returns
        ---------------------
        None
        '''

        self.current_value = self.initial_value
        self.status = 'normal'
        return