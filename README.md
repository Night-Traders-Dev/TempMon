### Raspberry Pi 4 HTTP Server for Sensor Data Visualization

This project allows a Raspberry Pi 4 to receive temperature, humidity, and magnetometer data from a Raspberry Pi Pico W over Wi-Fi, store the data, and generate real-time line charts. The charts are accessible via a web interface hosted on the RPi 4.

## Features

# HTTP Server:
A Flask-based server that receives data from the Pico W.

# Data Visualization:
Generates line charts for temperature, humidity, and magnetometer readings using Matplotlib.

# Web Interface:
Access the charts by navigating to the RPi 4's IP address.

# REST API:
POST endpoint for the Pico W to send sensor data.


## Requirements

Raspberry Pi 4 running Python 3.x

## Libraries:

* Flask

* Numpy

* Matplotlib



# Install the required Python libraries with:

```bash
pip install flask numpy matplotlib
```
## Setup Instructions

* 1. Clone the Repository:

```bash
git clone <repository_url>
cd <repository_name>
```


* 2. Run the Server:

```bash
python3 server.py
```

* 3. Access the Web Interface: Open your browser and navigate to
```bash
http://<RPi_IP>:5000/.
```


* 4. Send Data from Pico W: Ensure the Pico W is configured to send temperature, humidity, and magnetometer data to the RPi 4 using the provided API endpoint.



## API Endpoints

* 1. POST /data

Used by the Pico W to send sensor data.

```json
Request Body:

{
  "temperature": 72.5,
  "humidity": 45.3,
  "magnetometer": {"x": 1.23, "y": -0.87, "z": 0.45}
}
```
```json
Response:

{
  "status": "success"
}
```

* 2. GET /generate_charts

Generates line charts for temperature, humidity, and magnetometer data.

```json
Response:

{
  "status": "charts_generated"
}
```

* 3. GET /charts/<filename>

Serves the generated chart images.

```
Example: http://<RPi_IP>:5000/charts/temperature_chart.png
```

* 4. GET /

Displays the web interface with embedded charts.

## Usage

Navigate to the RPi 4's IP address (e.g., http://192.168.1.100:5000/) to view the charts.

The server will automatically process and visualize incoming data in real time.


License

This project is licensed under the MIT License. See the LICENSE file for more details.

