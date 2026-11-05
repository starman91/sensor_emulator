# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#		    		test_sensor.py
#
# Unit tests for the sensor simulator Sensor class.
#              -------------------
# author 	      : Robert White
# date           : Nov 4, 2026
# copyright   : (C) 2026 by  NLR
# email         : robert.white@nlr.gov
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import pytest
#Classes
from sensor_emulator.sensor import Sensor


#---------------------------------------------------------------------------------------
@pytest.fixture
def sensor_config():
    '''
    Provide a standard sensor configuration for testing.
    '''
    return {
        'sensor_id': 'ROOM101.TEMP',
        'sensor_type': 'temperature',
        'location_id': 'ROOM101',
        'unit': 'degC',
        'min_value': 18.0,
        'max_value': 26.0,
        'initial_value': 22.0,
        'target_value': 22.0,
        'noise_level': 0.1,
        'outdoor': False,
        'hadjacent': ['ROOM102'],
        'vhadjacent': []
    }


#---------------------------------------------------------------------------------------
@pytest.fixture
def sensor(sensor_config):
    '''Create a sensor instance for testing.'''

    return Sensor(config=sensor_config,random_seed=42)


# --------------------------------------------------
# Initialization tests
# --------------------------------------------------
def test_sensor_initialization(sensor):

    assert sensor.sensor_id == 'ROOM101.TEMP'
    assert sensor.sensor_type == 'temperature'
    assert sensor.location_id == 'ROOM101'
    assert sensor.unit == 'degC'

    assert sensor.min_value == 18.0
    assert sensor.max_value == 26.0

    assert sensor.initial_value == 22.0
    assert sensor.current_value == 22.0

    assert sensor.target_value == 22.0
    assert sensor.noise_level == 0.1

    assert sensor.status == 'normal'


# --------------------------------------------------
# Reading generation tests
# --------------------------------------------------
def test_sensor_update_returns_numeric_value(sensor):

    value = sensor.update()
    assert isinstance(value, float)


#---------------------------------------------------------------------------------------
def test_sensor_update_stays_within_range(sensor):

    for _ in range(1000):
        value = sensor.update()
        assert sensor.min_value <= value <= sensor.max_value


#---------------------------------------------------------------------------------------
def test_sensor_moves_toward_target(sensor):

    sensor.current_value = 20.0
    sensor.target_value = 24.0
    sensor.noise_level = 0.0
    value = sensor.update(alpha=0.1)

    assert value > 20.0
    assert value < 24.0


#---------------------------------------------------------------------------------------
def test_sensor_with_zero_noise(sensor):

    sensor.noise_level = 0.0
    sensor.current_value = 22.0
    sensor.target_value = 22.0
    value = sensor.update()

    assert value == 22.0


# --------------------------------------------------
# Configuration modification tests
# --------------------------------------------------
def test_set_target(sensor):

    sensor.set_target(24.0)
    assert sensor.target_value == 24.0

#---------------------------------------------------------------------------------------
def test_set_noise(sensor):

    sensor.set_noise(2.0)
    assert sensor.noise_level == 2.0


#---------------------------------------------------------------------------------------
def test_set_range(sensor):

    sensor.set_range(20.0, 30.0)
    assert sensor.min_value == 20.0
    assert sensor.max_value == 30.0


#---------------------------------------------------------------------------------------
def test_set_range_clamps_current_value(sensor):

    sensor.current_value = 25.0
    sensor.set_range(18.0, 22.0)
    assert sensor.current_value == 22.0


# --------------------------------------------------
# Error handling tests
# --------------------------------------------------

def test_invalid_range_raises_error(sensor):

    with pytest.raises(ValueError):
        sensor.set_range(26.0, 18.0)


def test_negative_noise_raises_error(sensor):

    with pytest.raises(ValueError):
        sensor.set_noise(-1.0)


# --------------------------------------------------
# Reset tests
# --------------------------------------------------

def test_sensor_reset(sensor):
    sensor.current_value = 25.0
    sensor.status = 'faulty'

    sensor.reset()

    assert sensor.current_value == sensor.initial_value
    assert sensor.status == 'normal'