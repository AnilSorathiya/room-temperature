# Room Temperature Docker Container

## Introduction

This is `room-temperature` a docker container that compute room temperature using ml model. This container provides endpoints to compute room temperature.

Please refer the [docker-compose.yml](docker-compose.yml) file for the configuration details.

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