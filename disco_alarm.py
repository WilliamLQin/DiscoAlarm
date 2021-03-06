from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from safe_schedule import SafeScheduler
from schedule import CancelJob
import threading
from traceback import format_exc

import disco_leds

scheduler = SafeScheduler()

end = False

endpoint = "a13a0acc0pv8gr.iot.us-east-1.amazonaws.com"
rootCAPath = "/home/pi/DiscoAlarm/root-CA.crt"
privateKeyPath = "/home/pi/DiscoAlarm/DiscoAlarm.private.key"
certificatePath = "/home/pi/DiscoAlarm/DiscoAlarm.cert.pem"
clientID = "21"

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientID)
myAWSIoTMQTTClient.configureEndpoint(endpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.connect()

# Pre Effect
def brighten(repeat, length):
	disco_leds.brighten(length)
	if not repeat:
		return CancelJob

# Alarm Light Patterns
def solid(repeat):
	disco_leds.solid()
	if not repeat:
		return CancelJob

def colorWipeForward(repeat):
	disco_leds.colorWipeForward()
	if not repeat:
		return CancelJob

def colorWipeBackward(repeat):
	disco_leds.colorWipeBackward()
	if not repeat:
		return CancelJob

def pingPong(repeat):
	disco_leds.pingPong()
	if not repeat:
		return CancelJob

def splashOut(repeat):
	disco_leds.splashOut()
	if not repeat:
		return CancelJob

def splashIn(repeat):
	disco_leds.splashIn()
	if not repeat:
		return CancelJob

def constellation(repeat):
	disco_leds.constellation()
	if not repeat:
		return CancelJob

# ----
def getFunc(name):
	func = None
	
	if name == "solid":
		func = solid
	elif name == "forward":
		func = colorWipeForward
	elif name == "backward":
		func = colorWipeBackward
	elif name == "pingpong":
		func = pingPong
	
	return func 

def callback(client, userdata, message):
	global end

        print "Information received:"
        print message.payload
        print "From topic:"
        print message.topic
        
        payload = message.payload
        params = payload.split()

	try:

		if params[0] == "end":
			end = True
			return

		if params[0] == "off":
			disco_leds.off()
			return

		post_effect = params[0]
		post_effect_start = params[1]
		pre_effect_duration = int(params[2]) * 60
		day = params[3]
		repeat = params[4]

		time = map(int, post_effect_start.split(":"))
		time[1] -= int(pre_effect_duration/60)
		if time[1] < 0:
			time[0] -= 1
			if time[0] < 0:
				time[0] = 23
			time[1] += 60
		
		pre_effect_start = str(time[0]) + ":" + str(time[1])

	except Exception:
		print format_exc()
		return

	func_pre = brighten
	func_post = getFunc(post_effect)
	
	rep = True if repeat == "yes" else False

	if day in ["sunday", "sundays", "weekend", "weekends"]:
		scheduler.every().sunday.at(pre_effect_start).do(func_pre, rep, pre_effect_duration)
		scheduler.every().sunday.at(post_effect_start).do(func_post, rep)				
	if day in ["monday", "mondays",  "weekday", "weekdays"]:
		scheduler.every().monday.at(pre_effect_start).do(func_pre, rep, pre_effect_duration)
		scheduler.every().monday.at(post_effect_start).do(func_post, rep)					
	if day in ["tuesday", "tuesdays", "weekday", "weekdays"]:
		scheduler.every().tuesday.at(pre_effect_start).do(func_pre, rep, pre_effect_duration)
		scheduler.every().tuesday.at(post_effect_start).do(func_post, rep)						
	if day in ["wednesday", "wednesdays", "weekday", "weekdays"]:
		scheduler.every().wednesday.at(pre_effect_start).do(func_pre, rep, pre_effect_duration)
		scheduler.every().wednesday.at(post_effect_start).do(func_post, rep)					
	if day in ["thursday", "thursdays", "weekday", "weekdays"]:
		scheduler.every().thursday.at(pre_effect_start).do(func_pre, rep, pre_effect_duration)
		scheduler.every().thursday.at(post_effect_start).do(func_post, rep)							
	if day in ["friday", "fridays", "weekday", "weekdays"]:
		scheduler.every().friday.at(pre_effect_start).do(func_pre, rep, pre_effect_duration)
		scheduler.every().friday.at(post_effect_start).do(func_post, rep)					
	if day in ["saturday", "saturdays", "weekend", "weekends"]:
		scheduler.every().saturday.at(pre_effect_start).do(func_pre, rep, pre_effect_duration)
		scheduler.every().saturday.at(post_effect_start).do(func_post, rep)	
			
myAWSIoTMQTTClient.subscribe("disco_alarm", 0, callback)
myAWSIoTMQTTClient.publish("connected", True, 0)

print "ready"

def clock_scheduler():
	global scheduler
	global end

	while not end:
		scheduler.run_pending()
		time.sleep(1)

def clock_leds():
	global end
	
	prev = time.time()

	while not end:
		elapsed = (time.time()-prev)*1000
		prev = time.time()
		disco_leds.clock(elapsed)
		time.sleep(0.001)

threading.Thread(target=clock_scheduler).start()
threading.Thread(target=clock_leds).start()

disco_leds.off()

#brighten(True, 60)
#pingPong(True)
