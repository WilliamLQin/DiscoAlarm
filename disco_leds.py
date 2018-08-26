import time
from neopixel import *
import argparse

LED_COUNT = 40
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
		if next[0] == "wait":
			internal_clock = next[1] - internal_clock - 1 - ms
			queue_position += 1
			continue
		else:	
			strip.setPixelColor(next[0], next[1])
			strip.show()
			internal_clock = next[2] - internal_clock - 1 - ms
			queue_position += 1

def off():
	global strip

	clear()

	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,0))
		strip.show()	

def clear():
	global call_queue
	global queue_position
	global internal_clock

	call_queue[:] = []
	queue_position = 0
	internal_clock = 0

def brighten(length):
	global strip
	global call_queue

	clear()

	wait = length*1000/256

	for i in range(256):
		fill(Color(i, i, i))
		call_queue.append(["wait", wait])

def dim (length):
	global strip
	global call_queue 

	clear()

	wait = length*1000/256

	for i in range(256):
		fill(Color(255-i, 255-i, 255-i))
		call_queue.append(["wait", wait])

def fill(color):
	global strip
	global call_queue

	for i in range(strip.numPixels()):
		call_queue.append([i, color, 0])

def solid():
	clear()
	fill(Color(255, 255, 200))

def colorWipe(color, wait_ms=50):
	global strip
	global call_queue

	for i in range(strip.numPixels()):
		call_queue.append([i, color, wait_ms])


