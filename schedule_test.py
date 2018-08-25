import pigpio
import time
from safe_schedule import SafeScheduler
from schedule import CancelJob

pi = pigpio.pi()
scheduler = SafeScheduler()

def good_task_1(t):
    print('Good Task 1 Runtime:', t)
    pi.write(18, 1)
    pi.write(15, 0)
    scheduler.every(t).seconds.do(good_task_1, t+1)
    return CancelJob

def good_task_2():
    print('Good Task 2')
    pi.write(18, 0)
    pi.write(15, 1)

def bad_task_1():
    print('Bad Task 1')
    print(1/0)

def bad_task_2():
    print('Bad Task 2')
    raise Exception('Something went wrong!')

scheduler.every(1).seconds.do(good_task_1, 2)
time.sleep(1)
scheduler.every(2).seconds.do(good_task_2)
scheduler.every(4).seconds.do(bad_task_2)

while True:
    scheduler.run_pending()
    time.sleep(1)
