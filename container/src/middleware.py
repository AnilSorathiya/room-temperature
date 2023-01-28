from flask import request
from .enums import APIParams
from .utils import watchdog as watchdog


def validate_request(*args):
    args_d = args[0]
    args_d = args_d[0].to_dict(flat=False)
    arguments = list(args_d.keys())
    errors = []
    data = {}

    # Model is designed for
    if (APIParams.ROOM_TEMPERATURE.value in arguments) and (len(args_d[APIParams.ROOM_TEMPERATURE.value]) > 0):
        room_temperature = args_d[APIParams.ROOM_TEMPERATURE.value][0]
        if (room_temperature is None) or (room_temperature == ""):
            errors.append({
                APIParams.ROOM_TEMPERATURE.value: "Not valid"
            })
        elif not (10.0 < float(room_temperature) < 50.0):
            errors.append({
                APIParams.ROOM_TEMPERATURE.value: "Not valid"
            })
        else:
            data[APIParams.ROOM_TEMPERATURE.value] = float(room_temperature)
    else:
        errors.append({
            APIParams.ROOM_TEMPERATURE.value: "is missing"
        })

    if (APIParams.LIGHT_BRIGHTNESS.value in arguments) and (
            len(args_d[APIParams.LIGHT_BRIGHTNESS.value]) > 0):
        light_brightness = args_d[APIParams.LIGHT_BRIGHTNESS.value][0]
        if (light_brightness is None) or (light_brightness == ""):
            errors.append({
                APIParams.LIGHT_BRIGHTNESS.value: "Not valid"
            })
        else:
            data[APIParams.LIGHT_BRIGHTNESS.value] = float(light_brightness)
    else:
        errors.append({
            APIParams.LIGHT_BRIGHTNESS.value: "is missing"
        })

    if (APIParams.PROCESSOR_TEMPERATURE.value in arguments) and (
            len(args_d[APIParams.PROCESSOR_TEMPERATURE.value]) > 0):
        processor_temperature = args_d[APIParams.PROCESSOR_TEMPERATURE.value][0]
        if (processor_temperature is None) or (processor_temperature == 0.0):
            errors.append({
                APIParams.PROCESSOR_TEMPERATURE.value: "Not valid"
            })
        else:
            data[APIParams.PROCESSOR_TEMPERATURE.value] = float(processor_temperature)
    else:
        errors.append({
            APIParams.PROCESSOR_TEMPERATURE.value: "is missing"
        })
    ## TODO remove this code
    # if (APIParams.FAMILY_DEVICE_ID.value in arguments) and (len(args_d[APIParams.FAMILY_DEVICE_ID.value]) > 0):
    #     family_device_id = args_d[APIParams.FAMILY_DEVICE_ID.value][0]
    #     if (family_device_id is None) or (family_device_id == ""):
    #         errors.append({
    #             APIParams.FAMILY_DEVICE_ID.value: "Not valid"
    #         })
    #     else:
    #         data[APIParams.FAMILY_DEVICE_ID.value] = str(family_device_id)
    # else:
    #     errors.append({
    #         APIParams.FAMILY_DEVICE_ID.value: "is missing"
    #     })

    if APIParams.HUB_HW_REVISION.value in arguments:
        allowed_revisions = ["1B", "2A", "2E"]
        hub_hw_revision = args_d[APIParams.HUB_HW_REVISION.value][0]
        if (hub_hw_revision is None) or (hub_hw_revision not in allowed_revisions):
            errors.append({
                APIParams.HUB_HW_REVISION.value: "Not valid. It must be one of: {0}".format(allowed_revisions)
            })
        else:
            data[APIParams.HUB_HW_REVISION.value] = str(hub_hw_revision)
    else:
        errors.append({
            APIParams.HUB_HW_REVISION.value: "is missing"
        })

    watchdog.logger.info(request.args)
    watchdog.logger.error(errors)

    return data, errors
