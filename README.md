# Room Temperature Docker Container


## Introduction
This is `room-temperature` a docker container that compute room temperature using ML model. This container provides
endpoints to compute room temperature. Please refer the [docker-compose.yml](docker-compose.yml) file for the configuration details.
This is simple example of linear model here. The model has been developed offline and used here to predict the 
room temperature value.

##TODO 
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


## Docker container requirements files

# Model 
## Assumptions
### Features used in the training data are in the following range:
* Temperature from temperature sensor is in range 10 to 45 degree celcius 
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

## Endpoints
### Room temperature
#### /calculate-room-temperature

Returns json data about room temperature, original hub temperature and device Id.

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
        curl -XGET http://localhost:8000/calculate-room-temperature?roomTemperature=28.875&lightBrightness=10&processorTemperature=34100
     ```
  