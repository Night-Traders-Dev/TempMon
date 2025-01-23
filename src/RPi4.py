from flask import Flask, request, jsonify, send_file, render_template_string
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Data storage
temperature_data = []
humidity_data = []

# HTML template to display the charts
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sensor Data Charts</title>
</head>
<body>
    <h1>Sensor Data Charts</h1>
    <p>Click on the charts to view/download full size.</p>
    <div>
        <h2>Temperature Over Time</h2>
        <a href="/charts/temperature_chart.png" target="_blank">
            <img src="/charts/temperature_chart.png" alt="Temperature Chart" style="width:70%;">
        </a>
    </div>
    <div>
        <h2>Humidity Over Time</h2>
        <a href="/charts/humidity_chart.png" target="_blank">
            <img src="/charts/humidity_chart.png" alt="Humidity Chart" style="width:70%;">
        </a>
    </div>
</body>
</html>
"""

@app.route('/data', methods=['POST'])
def receive_data():
    global temperature_data, humidity_data
    data = request.get_json()
    if 'temperature' in data and 'humidity' in data:
        temperature_data.append(data['temperature'])
        humidity_data.append(data['humidity'])
        print(f"Received: {data}")
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/generate_charts', methods=['GET'])
def generate_charts():
    global temperature_data, humidity_data

    # Create directories if not present
    os.makedirs("charts", exist_ok=True)

    # Generate temperature chart
    plt.plot(np.arange(len(temperature_data)), temperature_data, label='Temperature (F)', color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (F)")
    plt.title("Temperature Over Time")
    plt.legend()
    plt.savefig("charts/temperature_chart.png")
    plt.close()

    # Generate humidity chart
    plt.plot(np.arange(len(humidity_data)), humidity_data, label='Humidity (%)', color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Humidity (%)")
    plt.title("Humidity Over Time")
    plt.legend()
    plt.savefig("charts/humidity_chart.png")
    plt.close()

    return jsonify({"status": "charts_generated"}), 200

@app.route('/charts/<filename>')
def serve_chart(filename):
    chart_path = os.path.join("charts", filename)
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')
    return jsonify({"status": "error", "message": "Chart not found"}), 404

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
