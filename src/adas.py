# TFlite 기본 호출
import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util

# 기능용 호출
import track  # 추적 알고리즘
from cnr import real_coordinate  # 상태값 변환용 모듈
from cnr import determine_color

# 통신부도 따로 만들 것
import json
import urllib.request
import urllib.parse
import ssl
import math

# 기본 상수
FX = 640  # 프레임 크기 설정
FY = 480
ROI_LEN_X = 15  # roi 영역 크기 설정
ROI_LEN_Y = 15

# 검출 종류 별 ROI 영역 변수 , detect 종류  :  [roi x 중점 위치, roi y 중점 위치]
roi_dict = {
    'person': {'x': 1/2, 'y': 1/4},  # 사람의 경우 상의로 판단
    'dog': {'x': 1/2, 'y': 1/2},  # 강아지의 경우 중앙 지점으로 판단
    'car': {'x': 1/2, 'y': 1/2},
    'truck': {'x': 1/2, 'y': 1/2},
    'cat': {'x': 1/2, 'y': 1/2}
}
detect_list = list(roi_dict.keys())


#----- TFlite 기본 코드 시작 ------#

# 비디오 스트림 선언 부
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    # 라즈베리파이 카메라 초기화

    def __init__(self, resolution=(FX, FY), framerate=30):
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC,
                              cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])
        # 첫 프레임 읽기
        (self.grabbed, self.frame) = self.stream.read()
        # 카메라의 멈충 상태를 알려주는 변수
        self.stopped = False
    # 비디오 스트림으로 부터 프레임을 읽는 쓰레드를 시작시킴

    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    # 쓰레드가 중단될때 까지 계속 되는 업데이트 부분

    def update(self):
        while True:
            # 카메라가 멈추면 쓰레드 중단
            if self.stopped:
                self.stream.release()
                return
            # 아니면 프레임을 계속 해서 읽는다
            (self.grabbed, self.frame) = self.stream.read()
    # 가장 최근 프레임을 반환한다.

    def read(self):
        return self.frame
    # 멈춤

    def stop(self):
        self.stopped = True


# TFlite 모델 및 edgetpu argument 선언부
parser = argparse.ArgumentParser()
parser.add_argument(
    '--modeldir', help='Folder the .tflite file is located in', required=True)
parser.add_argument(
    '--graph', help='Name of the .tflite file, if different than detect.tflite', default='detect.tflite')
parser.add_argument(
    '--labels', help='Name of the labelmap file, if different than labelmap.txt', default='labelmap.txt')
parser.add_argument(
    '--threshold', help='Minimum confidence threshold for displaying detected objects', default=0.5)
parser.add_argument(
    '--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.', default='640x480')
parser.add_argument(
    '--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection', action='store_true')
args = parser.parse_args()
MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = args.edgetpu

# TF 라이브러리 호출 본 프로젝트의 경우 use_TPU 부분을 사용한다고 생각하면 된다.
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate
# TPU 모델을 사용할 경우 모델 명 변경
if use_TPU:
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'

# 현재 디렉토리의 경로를 불러옴
CWD_PATH = os.getcwd()
# 객체 검출에 쓰일 tflite 모델 파일의 경로를 저장
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)
# 객체 검출에 쓰일 라벨맵 파일의 경로를 저장
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# 라벨 맵을 불러옴, 첫번째 라벨이 ??? 인 경우가 있어서 지워야한다고함
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]
if labels[0] == '???':
    del(labels[0])

# TPU를 사용할 경우 특별한 load_delegate argument를 사용함
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT, experimental_delegates=[
                              load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

# 모델의 세부사항을 불러온다.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
floating_model = (input_details[0]['dtype'] == np.float32)
input_mean = 127.5
input_std = 127.5

# frame rate를 위한 변수들 선언
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# 이제 비디오 스트림을 생성한다.
videostream = VideoStream(resolution=(imW, imH), framerate=30).start()

#----- TFlite 기본 코드 끝 ------#


#-----     로직 시작     ------#

f = open("debuger.txt", 'w')
# 작동 변수 선언
exists = {}
for label in detect_list:
    exists[label] = []

# 모터 초기화
while True:

     #-----1. 검출부    ------#

    # fps 측정 용 타이머 시작
    t1 = cv2.getTickCount()
    # 현재 프레임을 읽어옴
    frame1 = videostream.read()
    # 프레임 사이즈 재조정 부분
    # 현재 프로젝트에서는 640*480을 그대로 사용중이기 때문에 빼도 될수도있음
    frame = frame1.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR 로 읽어온걸 RGB로 바꿈
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)
    # floating model 사용시 픽셀 값을 정규화 함.
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # 모델을 사용해서 검출하는 부분.
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # 검출 결과를 받아온다.
    # Bounding box coordinates of detected objects
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[
        0]  # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[
        0]  # Confidence of detected objects
    gridbox = []  # [ymin,xmin,ymax,xmax] 를 포함해서 확장을 위해 종류도 넣으면 좋을 것으로 보임

    for i in range(len(scores)):
        if ((scores[i] > 0.4) and (scores[i] <= 1.0) and labels[int(classes[i])] in detect_list):
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))
            # 그리드 박스에 좌측 상단, 우츤 하단 점을 저장한다
            gridbox.append([ymin, xmin, ymax, xmax, labels[int(classes[i])]])
    #----- 2. 상태값 추출부   ------#

    # 상태값 변수 초기화 , 이것도 전부 딕셔너리로 하는게 나을거같단 생각이..
    values = {}
    cnt = {}
    for label in detect_list:
        values[label] = []
        cnt[label] = -1

    for ymin, xmin, ymax, xmax, label in gridbox:

        cnt[label] = cnt[label]+1

        # Calibration
        values[label].append({cnt[label]: {}})
        values[label][cnt[label]]['point'] = real_coordinate(
            [xmin, FY-ymax], [xmax, FY-ymax])  # 하단 중앙점의 현실 좌표계를 반환합니다
        values[label][cnt[label]]['gridbox'] = [ymin, xmin, ymax, xmax]
        # ROI RGB
        roi_px = int((xmin+xmax) * roi_dict[label]['x'])
        roi_py = int((ymin+ymax) * roi_dict[label]['y'])
        roi_color = []
        for i in range(roi_px-ROI_LEN_X, roi_px+ROI_LEN_X+1):
            for j in range(roi_py-ROI_LEN_Y, roi_py+ROI_LEN_Y+1):
                if i >= 0 and i <= FX and j >= 0 and j <= FY:
                    roi_color.append(frame[j][i])
        values[label][cnt[label]]['color'] = determine_color(roi_color)

    #----- 3. 추적 알고리즘 시행, cv2를 통한 라벨 생성부   ------#
    # 추적 알고리즘 시행
    exists, dir, crush_time = track.track(exists, values, detect_list)
    # 여기는 그리드를 하기 보다는 충돌 시간에 맞춰서 제동 혹은 경고음을 올리는게 더 좋을것으로 생각됨. 그리드는 단순히 판단용
    # cv2로 그리드
    server_label = {}
    for object_label in detect_list:
        exist_list = exists[object_label]
        LEN_EXIST = len(exist_list)
        for i in range(LEN_EXIST):
            if exist_list[i].detect == True:
                ymin, xmin, ymax, xmax = exist_list[i].gridbox
                x, y = exist_list[i].point
                object_name = object_label + str(exist_list[i].number)
                label = '%s: x: %.2f m , y: %.2f m' % (
                    object_name, x, y)  # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                # Make sure not to draw label too close to top of window
                label_ymin = max(ymin, labelSize[1] + 10)
                server_label[object_name] = {
                    'x': xmin, 'y': label_ymin-labelSize[1]-10}
                # Draw white box to put label text in
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (
                    xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
                # Draw label textcv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                cv2.putText(frame, label, (xmin, label_ymin-7),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # FPS 계산 라벨 작성
    cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
    # 프레임 출력, (스트리밍 시 스트리밍 부로 변경할 것, 현재는 테스트 환경이기 때문에 라즈베리파이를 통해 출력)
    cv2.imshow('Object detector', frame)
    # framerate 계산
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc = 1/time1

    # 강제 종료 키
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
videostream.stop()
