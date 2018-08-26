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

for i in range(strip.numPixels()):
	strip.setPixelColor(i, Color(255, 0, 0))

strip.show()
