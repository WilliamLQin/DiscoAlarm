import time
from neopixel import *
import argparse

LED_COUNT = 40
LED_PIN = 18

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 200
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

for i in range(strip.numPixels()):
	strip.setPixelColor(i, Color(50, 255, 0))

strip.setPixelColor(2, Color(100, 100, 255))
strip.setPixelColor(10, Color(100, 100, 255))
strip.setPixelColor(13, Color(100, 100, 255))
strip.setPixelColor(30, Color(100, 100, 255))


strip.show()

x = strip.getPixelColor(2)
print x
print hex(x)

strip.setPixelColor(0, x)
#strip.setPixelColor(38, hex(x))
strip.setPixelColor(38, int(hex(x), 16))

strip.setPixelColor(39, Color(50, 255, 0))

strip.show()
