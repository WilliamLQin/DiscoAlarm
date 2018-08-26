from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from safe_schedule import SafeScheduler
from schedule import CancelJob
import threading

import disco_leds_test as disco_leds

scheduler = SafeScheduler()

end = False

endpoint = "a13a0acc0pv8gr.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
privateKeyPath = "DiscoAlarm.private.key"
certificatePath = "DiscoAlarm.cert.pem"
clientID = "23"

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientID)
myAWSIoTMQTTClient.configureEndpoint(endpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.connect()

def leds_brighten(length):
	disco_leds.brighten(length)
	return CancelJob

def leds_dim(length):
	disco_leds.dim(length)
	return CancelJob

def callback(client, userdata, message):
	global end

        print "Information received:"
        print message.payload
        print "From topic:"
        print message.topic
        
        payload = message.payload
        params = payload.split()

	print time.time()

	if params[0] == "end":
		end = True

        if len(params) == 2:
                if params[0] == "brighten":
                        scheduler.every(1).seconds.do(leds_brighten, float(params[1]))
                elif params[0] == "dim":   
                        scheduler.every(1).seconds.do(leds_dim, float(params[1]))

myAWSIoTMQTTClient.subscribe("disco_alarm", 0, callback)

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
