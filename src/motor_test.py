import RPi.GPIO as GPIO  # RPi.GPIO 라이브러리를 GPIO로 사용
from time import sleep  # time 라이브러리의 sleep함수 사용


'''
서보 위치 제어 함수
degree에 각도를 입력하면 duty로 변환후 서보 제어(ChangeDutyCycle)
'''


def duty_maker(degree):
    SERVO_MAX_DUTY = 12.5  # 서보의 최대(180도) 위치의 주기s
    SERVO_MIN_DUTY = 3.5    # 서보의 최소(0도) 위치의 주기
    duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/138.0)
    return duty


def camera_motor_control():
    # 각도는 180도를 넘을 수 없다.
    servoPin = 17   # 서보 핀
    GPIO.setmode(GPIO.BCM)        # GPIO 설정nchips
    GPIO.setup(servoPin, GPIO.OUT)  # 서보핀 출력으로 설정
    servo = GPIO.PWM(servoPin, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
    servo.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.

    servo.ChangeDutyCycle(duty_maker(30))
    sleep(0.5)
    servo.ChangeDutyCycle(duty_maker(100))
    sleep(0.5)
    servo.ChangeDutyCycle(duty_maker(30))
    sleep(0.5)
    servo.ChangeDutyCycle(duty_maker(100))
    sleep(0.5)
    GPIO.cleanup()
    return


camera_motor_control()
