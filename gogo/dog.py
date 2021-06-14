#-*- coding: utf-8 -*-

# 라즈베리파이 GPIO 패키지 
import RPi.GPIO as GPIO
from time import sleep

import sys
from socket import *
from select import *
import cv2

HOST = '127.0.0.1'
PORT = 10001
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 생성
serverSocket = socket(AF_INET, SOCK_STREAM)

# 소켓 주소 정보 할당
serverSocket.bind(ADDR)
print('bind')

# 연결 수신 대기 상태
serverSocket.listen(100)
print('listen')

# 연결 수락
clientSocekt, addr_info = serverSocket.accept()
print('accept')
print('--client information--')
print(clientSocekt)
sys.stdout.flush()

# 클라이언트로부터 메시지를 가져옴

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWORD = 2

# 모터 채널
CH1 = 0
CH2 = 1

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
#PWM PIN
ENA = 26  #37 pin
ENB = 0   #27 pin

#GPIO PIN
IN1 = 19  #37 pin
IN2 = 13  #35 pin
IN3 = 6   #31 pin
IN4 = 5   #29 pin

# 핀 설정 함수
def setPinConfig(EN, INA, INB):        
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    # 100khz 로 PWM 동작 시킴 
    pwm = GPIO.PWM(EN, 100) 
    # 우선 PWM 멈춤.   
    pwm.start(0) 
    return pwm

# 모터 제어 함수
def setMotorContorl(pwm, INA, INB, speed, stat):

    #모터 속도 제어 PWM
    pwm.ChangeDutyCycle(speed)  
    
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
        
    #뒤로
    elif stat == BACKWORD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
        
    #정지
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)

        
# 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor(ch, speed, stat):
    if ch == CH1:
        #pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmA, IN1, IN2, speed, stat)
    else:
        #pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmB, IN3, IN4, speed, stat)
  

# GPIO 모드 설정 
GPIO.setmode(GPIO.BCM)
      
#모터 핀 설정
#핀 설정후 PWM 핸들 얻어옴 
pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

#제어 시작
n = 0
speed1 = 70
speed2 = 70
try:
# 앞으로 100프로 속도로
    while True:
        setMotor(CH1, speed1, FORWARD)
        setMotor(CH2, speed2, FORWARD)
        sleep(0.01)
        data = clientSocekt.recv(1000) 
        print('recieve data : ',data.decode())
        msg = data.decode()
        if msg == 'person': 
            setMotor(CH1, 0, FORWARD)
            setMotor(CH2, 0, FORWARD)
            sleep(3)
        elif msg == 'stop sign' :
            setMotor(CH1, 0, FORWARD)
            setMotor(CH2,0, FORWARD)
            sleep(5)
        else :
            speed1 = 70
            speed2 = 70
        msg = "default"
        
        if cv2.waitKey(1) == ord('q'):
            break            


    
except KeyboardInterrupt:
    sys.exit(1)
    
clientSocekt.close()
serverSocket.close()
'''
# 뒤로 40프로 속도로
setMotor(CH1, 40, FORWARD)
setMotor(CH2, 40, FORWARD)
sleep(5)

# 뒤로 100프로 속도로
setMotor(CH1, 50, FORWARD)
setMotor(CH2, 50, BACKWORD)
sleep(5)

#정지 
setMotor(CH1, 80, STOP)
setMotor(CH2, 80, STOP)
# 종료
'''
GPIO.cleanup()
