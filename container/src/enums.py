from enum import Enum

# This is central location of all fixed variables used room temperature ML container.
# The variable creates link between database(through elastic search query) and model
# input features as well as APIs parameters.


class APIParams(Enum):
    ROOM_TEMPERATURE = 'roomTemperature'
    LIGHT_BRIGHTNESS = 'lightBrightness'
    PROCESSOR_TEMPERATURE = 'processorTemperature'
    HUB_HW_REVISION = 'hubHWRevision'


class ESColumns(Enum):
    ROOM_TEMPERATURE = 'doc.roomTemperature'
    LIGHT_BRIGHTNESS = 'doc.lightBrightness'
    PROCESSOR_TEMPERATURE = 'doc.processorTemperature'
    DEVICE_TYPE = 'extra.device.type'


class ModelColumns(Enum):
    AVG_ROOM_TEMPERATURE = 'avgRoomTemperature'
    AVG_LIGHT_BRIGHTNESS = 'avgLightBrightness'
    AVG_PROCESSOR_TEMPERATURE = 'avgProcessorTemperature'

