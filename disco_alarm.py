from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import pigpio
import time
from safe_schedule import SafeScheduler
from schedule import CancelJob

pi = pigpio.pi()
scheduler = SafeScheduler()

endpoint = "a13a0acc0pv8gr.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
privateKeyPath = "DiscoAlarm.private.key"
certificatePath = "DiscoAlarm.cert.pem"
clientID = "23"

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientID)
myAWSIoTMQTTClient.configureEndpoint(endpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.connect()

def light_led(switch, gpio):
        pi.write(gpio, switch)

def led_job(switch, gpio):
	light_led(switch, gpio)
	return CancelJob

def callback(client, userdata, message):
        print "Information received:"
        print message.payload
        print "From topic:"
        print message.topic
        
        payload = message.payload
        params = payload.split()

        if message.topic == "led":
                if params[1] == "on":
                        scheduler.every(1).seconds.do(led_job, 1, int(params[0]))
                elif params[1] == "off":   
                        scheduler.every(1).seconds.do(led_job, 0, int(params[0]))

myAWSIoTMQTTClient.subscribe("led", 0, callback)

print "ready"

while True:
	scheduler.run_pending()
	time.sleep(1)

