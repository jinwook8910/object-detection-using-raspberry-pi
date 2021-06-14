from gpiozero import Robot

import time



dc_motor = Robot(left=(19, 13), right=(6, 5))



for num in range(4):



	dc_motor.forward(speed=1)

	time.sleep(3)




	dc_motor.stop()

	time.sleep(0.5)




	dc_motor.backward(speed=0.5)

	time.sleep(3)



dc_motor.stop()
