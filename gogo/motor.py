from gpiozero import Motor
import time

motor = Motor(forward=20, backward=21)

while True:
	motor.forward()
	time.sleep(5)

 
