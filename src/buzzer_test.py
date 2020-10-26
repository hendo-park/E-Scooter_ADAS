import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) #불필요한 warning제거
GPIO.setmode(GPIO.BCM) #GPIO모드 설정

GPIO.setup(22,GPIO.OUT) 
p=GPIO.PWM(22,100) #18번 핀, 주파수 =100Hz

B = [392, 330, 330, 349, 294, 294, 262, 294, 330, 349, 392, 392]
#솔미미 파레레 도레미파솔솔솔
speed = 0.7 #음과 음사이 시간 0.7
p.start(10) #PWM시작, 듀티사이클 10

try:
    while 1:
        for b in B: 
            p.ChangeFrequency(b) #주파수로 변경
            time.sleep(speed) #0.7초동안 일시정지 => 음과 음사이 시간

except KeyboardInterrupt: #ctrl + C하면 빠져나옴
    pass
p.stop() 