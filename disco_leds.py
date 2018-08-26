import time
from neopixel import *
import argparse

LED_COUNT = 10
LED_PIN = 18

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

internal_clock = 0
call_queue = []
queue_position = 0

def clock(ms):
	global internal_clock
	global call_queue
	global queue_position
	global strip

	if len(call_queue) > 0 and internal_clock > 0:
		internal_clock -= ms

	while internal_clock <= 0 and queue_position < len(call_queue):
		next = call_queue[queue_position]
		if next[0] == "goto":
			queue_position = next[1]
			continue
		strip.setPixelColor(next[0], next[1])
		strip.show()
		internal_clock = next[2] - 2*internal_clock - ms
		queue_position += 1

def off():
	global strip

	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,0))
		strip.show()	

def clear():
	global call_queue
	global queue_position

	call_queue[:] = []
	queue_position = 0

def colorWipe(color, wait_ms=50):
	global strip
	global call_queue

	for i in range(strip.numPixels()):
		call_queue.append([i, color, wait_ms])
