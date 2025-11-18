"""
LCD display logic for rudder position
"""

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
import time
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7789
from datetime import datetime
import math

width = 128
height = 128

serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25, bus_speed_hz=52000000)
device = st7789(serial_interface=serial, width=width, height=height, rotate=1)
device.clear()

CLK_PIN = 17  # CLK
DT_PIN = 27  # DT
SW_PIN = 22  # Switch / push button

GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

import threading

counter = 0
last_clk_state = GPIO.input(CLK_PIN)

min_degree = -60
max_degree = 60
steps = 30
counter_to_degree = max_degree / steps  # 240 steps from -120 to 120
max_counter = steps
min_counter = -steps

counter_lock = threading.Lock()


def get_rudder_angle(counter):
    return counter * counter_to_degree


def draw_loop():
    while True:
        with counter_lock:
            local_counter = counter
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
            cx, cy = width // 2, height // 2 + 20  # Move center down by 20 pixels
            radius = min(width, height) // 2 - 10

            # Draw rudder arc (from -60 to +60 degrees)
            draw.arc(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                start=-150,  # -60 degrees rudder = -150 in arc coordinates (since -90 offset)
                end=-30,  # +60 degrees rudder = -30 in arc coordinates
                fill="white",
                width=2,
            )

            # Get rudder angle
            rudder_angle = get_rudder_angle(local_counter)

            # Draw rudder direction indicator (pointing up = straight, rotates with rudder angle)
            rudder_rad = math.radians(
                rudder_angle - 90
            )  # -90 to make 0 degrees point up
            indicator_len = radius * 0.8
            draw.line(
                [
                    cx,
                    cy,
                    cx + indicator_len * math.cos(rudder_rad),
                    cy + indicator_len * math.sin(rudder_rad),
                ],
                fill="yellow",
                width=8,
            )

            # Draw center dot
            draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill="yellow")

            # Draw angle markers at min, 0, and max rudder angles
            for angle in [min_degree, 0, max_degree]:
                marker_rad = math.radians(angle - 90)
                marker_start = radius * 0.85
                marker_end = radius * 0.95
                x1 = cx + marker_start * math.cos(marker_rad)
                y1 = cy + marker_start * math.sin(marker_rad)
                x2 = cx + marker_end * math.cos(marker_rad)
                y2 = cy + marker_end * math.sin(marker_rad)
                draw.line([x1, y1, x2, y2], fill="white", width=2)

            # Display rudder angle as text (larger font in freed up space)
            draw.text((10, 5), f"{rudder_angle:.1f}°", fill="yellow")
        time.sleep(0.01)


draw_thread = threading.Thread(target=draw_loop, daemon=True)
draw_thread.start()

while True:
    clk_state = GPIO.input(CLK_PIN)
    dt_state = GPIO.input(DT_PIN)
    sw_state = GPIO.input(SW_PIN)
    if clk_state != last_clk_state:
        with counter_lock:
            if dt_state != clk_state:
                counter += 1
            else:
                counter -= 1
            if counter < min_counter:
                counter = min_counter
            if counter > max_counter:
                counter = max_counter
    last_clk_state = clk_state
    if sw_state == 0:
        with counter_lock:
            counter = 0
    time.sleep(0.001)
