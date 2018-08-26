import pigpio
import time

pi = pigpio.pi()

internal_clock = 0
call_queue = []
queue_position = 0

def clock(ms):
	global internal_clock
	global call_queue
	global queue_position

	if queue_position < len(call_queue):
		internal_clock -= ms

	while internal_clock <= 0 and queue_position < len(call_queue):
		next = call_queue[queue_position]
		if next[0] == "goto":
			queue_position = next[1]
			continue
		pi.set_PWM_dutycycle(18, next[0])
		internal_clock = next[1] + internal_clock - 1 - ms 
		queue_position += 1
		
		if queue_position == len(call_queue) - 1:
			print time.time()


def clear():
	global call_queue
	global queue_position

	call_queue[:] = []
	queue_position = 0

def mode_brightness(length):
	queue = []
	
	wait = length*1000/256

	for i in range(256):
		queue.append([i, wait])

	return queue

def brighten(length):
	global call_queue
	
	clear()

	queue = mode_brightness(length)
	
	for command in queue:
		call_queue.append(command)

def dim(length):
	global call_queue

	clear()

	queue = mode_brightness(length)

	for command in reversed(queue):
		call_queue.append(command)	

