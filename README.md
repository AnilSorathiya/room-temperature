# Room Temperature Model and Docker Container

## Introduction
Temperature sensors provides good accuracy when you use in control variables. However, when you embedded into a hardware
device, there are other variables affect the reading of the sensor such as processor temperature, external temperature,
any LED attach with the device.

This is `room-temperature` docker container that compute room temperature using ML model taking as input of above 
variables. This container provides endpoints so that it can be easy deployed and call from user interface/app or even 
internal infrastructure services for further complex computation.
Please refer the [docker-compose.yml](container/docker-compose.yml) file for the configuration details. This is simple example of 
linear model here. The model has been developed offline and used here to predict the room temperature value through API 
call.

## Folder structure:
```
--container: Docker container source code
    --model: model used by in production
    --src: source code APIs and model wrapper to run in docker container
        --utils: utility modules
    --test: container tests
    (docker cofiguration files)
--data: data folder
--notebooks: exploratory analysis of room temperature and offline model building
    --models: store relevant models
README.md:  readme file
```

# Model 
## Assumptions
### Features used in the training data are in the following range:
* Temperature from temperature sensor is in range 10 to 45 degree Celsius 
* Light brightness level of device is in range of 0 to 100 
* Processor temperature of device is in range of 31000 to 45000

## Tools
**uWSGI**
---
The `run_service.sh` starts uWSGI service to manage containers rest api application. The configuration parameters
for the uWSGI can be found in the `wsgi.ini` file.

`wsgi.ini`:

```ini
[uwsgi]
http-socket = :8000
plugin      = python
wsgi-file   = ./routes.py
process     = 5
callable    = app
```

---

## Execution steps

1. Build and run docker container
```commandline
    cd <path-to-container-folder>
    docker-compose up
```
2.  Browser url 
    http://localhost:8001/calculate-room-temperature?roomTemperature=30.25&lightBrightness=40&processorTemperature=33600&hubHWRevision=2E
    
    or
    
    Use the following curl command on terminal:
```commandline
    curl --location --request GET 'http://localhost:8001/calculate-room-temperature?roomTemperature=30.25&lightBrightness=40&processorTemperature=33600&hubHWRevision=2E'  
```


## Endpoints
### Room temperature
#### /calculate-room-temperature

Returns json data about room temperature, original hub temperature and device id.

* **URL**
  `http://<host>:<port>/calculate-room-temperature`

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `roomTemperature=[float]` Current room temperature from `temperature sensor`

   `lightBrightness=[integer]` Current light brightness level of device

   `processorTemperature=[int]` Current processor temperature of device

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json
    {
      "originalInputTemperature": 28.875,
      "roomTemperature": 22.11831923986586
    }
    ```

* **Error Response:**

  * **Code:** 400 Bad Request <br />

* **Sample Call:**

     ```bash
        curl -XGET http://localhost:8001/calculate-room-temperature?roomTemperature=28.875&lightBrightness=10&processorTemperature=34100
     ```
  