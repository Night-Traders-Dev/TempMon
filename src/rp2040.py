import board
import busio
import neopixel
import time
import wifi
import socketpool
import adafruit_requests

from adafruit_sht31d import SHT31D
from adafruit_ssd1306 import SSD1306_I2C

# Initialize NeoPixel
pixels = neopixel.NeoPixel(board.GP0, 1)

# Initialize I2C and sensor
i2cl = busio.I2C(scl=board.GP17, sda=board.GP16)
i2c0 = busio.I2C(scl=board.GP15, sda=board.GP14)
display = SSD1306_I2C(128, 64, i2c0)
sht_sensor = SHT31D(i2cl)

# Wi-Fi setup
wifi.radio.connect("ssid", "password")
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, None)

# Function to convert Celsius to Fahrenheit
def c_to_f(temp):
    return (temp * 9/5) + 32

# Function to map temperature to RGB color
def temperature_to_color(temp_f):
    color_map = [
        (0, (0, 0, 255)),
        (10, (0, 128, 255)),
        (20, (0, 255, 255)),
        (30, (0, 255, 128)),
        (40, (0, 255, 0)),
        (50, (128, 255, 0)),
        (60, (255, 255, 0)),
        (70, (255, 128, 0)),
        (80, (255, 0, 0)),
        (90, (128, 0, 128)),
        (100, (255, 0, 255))
    ]
    for i in range(len(color_map) - 1):
        if color_map[i][0] <= temp_f < color_map[i + 1][0]:
            t1, c1 = color_map[i]
            t2, c2 = color_map[i + 1]
            ratio = (temp_f - t1) / (t2 - t1)
            r = int(c1[0] + ratio * (c2[0] - c1[0]))
            g = int(c1[1] + ratio * (c2[1] - c1[1]))
            b = int(c1[2] + ratio * (c2[2] - c1[2]))
            return (r, g, b)
    if temp_f < color_map[0][0]:
        return color_map[0][1]
    elif temp_f > color_map[-1][0]:
        return color_map[-1][1]

def display_text(str, line):
    display.text(str, 0, (line % 8) * 8, 1, font_name="/lib/font5x8.bin")

# Main loop
while True:
    display.fill(0)
    temp_c = sht_sensor.temperature
    humi = sht_sensor.relative_humidity
    temp_f = c_to_f(temp_c)
    color = temperature_to_color(temp_f)
    pixels[0] = color
    display_text(f"Temperature: {temp_f:.2f}F", 0)
    display_text(f"Humidity: {humi:.2f}%", 2)
    display.show()

    # Send data to Raspberry Pi
    try:
        response = requests.post(
            "http://x.x.x.x:5000/data",
            json={"temperature": temp_f, "humidity": humi}
        )
        print(f"Sent data, response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {e}")

    time.sleep(1)
