import adas_matching
import math
from similarity import cosine_map
from similarity import cos_similarity
import time
import impact
import datetime
import copy
import collections as col
WINDOW_SIZE = 30  # (20fps 기준 약 1.5초)
DISTANCE = 30


class detect_object:
    def __init__(self, label, number, value):
        # 검출 객체 종류
        self.label = label
        self.number = number
        # 상태값 초기화
        self.point = value['point']  # 현재 좌표값
        self.color = value['color']  # 색
        self.gridbox = value['gridbox']
        self.timer = time.time()  # 감지된 시간
        self.detect = True
        self.path = col.deque(maxlen=WINDOW_SIZE)
        self.path.append([self.point, self.timer])
        self.midpoint = [0, 0]
        self.vector = [0, 0]
        self.crush_level = 0  # 최고 레벨 3. 3일 경우 제동이 들어가야함
        self.crush_time = 999999
        self.crush_dir = 'Middle'

    def path_update(self, value):
        temp_point = value['point']
        temp_timer = time.time()
        if len(self.path) < WINDOW_SIZE:
            self.path.append([temp_point, temp_timer])
            self.midpoint = [(self.midpoint[0] + temp_point[0])/len(self.path),
                             (self.midpoint[1] + temp_point[1])/len(self.path)]
            self.timer = temp_timer
        else:
            if cos_similarity(temp_point, self.midpoint) < DISTANCE:
                past_point, past_time = self.path.popleft()
                self.midpoint = [(self.midpoint[0] + (temp_point[0]-past_point[0]))/len(
                    self.path), (self.midpoint[1] + (temp_point[1]-past_point[1]))/len(self.path)]
                self.path.append([temp_point, temp_timer])
                self.point = temp_point
                self.timer = temp_timer

    def update(self, value):
        self.color = value['color']
        self.gridbox = value['gridbox']
        self.detect = True
        # 여기서 벡터 결정하는 함수를 사용해서, 벡터를 결정한다. 벡터의 결정을 원할때는 최소한 path의 길이가 어느 수준 이상이여야할 것.
        if len(self.path) == WINDOW_SIZE:
            temp_path = []
            for i in range(WINDOW_SIZE):
                temp = self.path.popleft()
                temp_path.append(temp)
                self.path.append(temp)

            # 6개정도 단위로 잘라서 벡터 평균을 구해본다
            NEXT_TIME = 10
            m_v_x = 0
            m_v_y = 0
            cnt = 0
            for i in range(WINDOW_SIZE):
                for j in range(i+1, WINDOW_SIZE):
                    v_x = temp_path[i][0][0] - temp_path[j][0][0]
                    v_y = temp_path[i][0][1] - temp_path[j][0][1]
                    v_t = temp_path[j][1] - temp_path[i][1]
                    m_v_x = m_v_x + (v_x/v_t)
                    m_v_y = m_v_y + (v_y/v_t)
                    cnt = cnt + 1
            self.vector = [round(m_v_x/cnt, 3), round(m_v_y/cnt, 3)]

            self.crush_dir, self.crush_time = impact.impact(
                self.point, self.vector)

        # 충돌 시간도 바로 판단해 준다.

    # 확장형 칼만 필터 예측 및 수정 부분
    # def ekf_predict(self) :
    # def ekf_correct(self) :


def char_changer(map):
    n = len(map)
    p_map = ""
    for i in range(n):
        for j in range(len(map[i])):
            p_map = p_map + str(round(map[i][j], 1)) + " "
        p_map = p_map + '\n'
    return p_map


def track(exists, values, detect_list):
    f = open("debuger.txt", 'a')

    min_crush_time = 999999
    c_dir = 'Middle'
    for object_label in detect_list:
        exist_list = exists[object_label]  # 얘는 class
        value_list = values[object_label]  # 얘는 딕셔너리 형태
        LEN_EXIST = len(exist_list)
        LEN_NEW = len(value_list)
        # 번호 지정
        deq = col.deque()
        numberlist = [False for i in range(11)]
        for i in range(LEN_EXIST):
            numberlist[exist_list[i].number] = True
        for i in range(1, 11):
            if numberlist[i] == False:
                deq.append(i)

        # color 맵 구성
        exist_color = []
        for i in range(LEN_EXIST):
            exist_color.append(exist_list[i].color)
        new_color = []
        for i in range(LEN_NEW):
            new_color.append(value_list[i]['color'])
        color_map = cosine_map(exist_color, new_color)
        # color 에 의한 헝가리안 매칭, 거리가 일정 수준 이하인 매칭의 경우 따로 빼줄 수 있도록 한다.

        # xy coordinate 맵 구성

        exist_point = []
        for i in range(LEN_EXIST):
            exist_point.append(exist_list[i].point)  # 일단 현재 지점만 가지고 해보자

        # 측정지점의 경우 그대로 사용한다
        new_point = []
        for i in range(LEN_NEW):
            new_point.append(value_list[i]['point'])

        xy_map = cosine_map(exist_point, new_point)

        # 매칭을 실행한다
        update_exist = []
        match = adas_matching.matching(color_map, xy_map)

        for past, now in match:
            if (past == -1 or past >= LEN_EXIST) and now < LEN_NEW and now != -1:
                # 새로운 객체를 생성한다
                exist_list.append(detect_object(
                    object_label, deq.popleft(), value_list[now]))
                # 벡터 생성 최대한 멋지게
                update_exist.append(len(exist_list)-1)

            elif now < LEN_NEW and now != -1:
                # 존재하던 객체를 갱신한다
                 # 벡터 생성 최대한 멋지게
                # exist_list[past].path_update(value_list[now])
                # exist_list[past].update(value_list[now])

                # 벡터 생성 최대한 간단하게

                temp_time = exist_list[past].timer - time.time()
                exist_list[past].timer = time.time()
                temp_x = exist_list[past].point[0]-value_list[now]['point'][0]
                temp_y = exist_list[past].point[1]-value_list[now]['point'][1]
                exist_list[past].vector = [
                    round(temp_x/temp_time, 3), round(temp_y/temp_time, 3)]
                exist_list[past].point = value_list[now]['point']
                exist_list[past].gridbox = value_list[now]['gridbox']
                exist_list[past].crush_dir, exist_list[past].crush_time = impact.impact(
                    exist_list[past].point, exist_list[past].vector)
                exist_list[past].detect = True
                update_exist.append(past)

                print(exist_list[past].vector)
                print(round(exist_list[past].crush_time, 3))
                # 벡터가 일정 기준 이상 모였을 경우 -> 벡터를 포함해서 판단한다.

        # 현재 검출되지 않은 객체의 경우 실존하지 않음은 알려줘야한다 (왜냐하면 그걸로 멈출순 없으니까)
        temp_exist_list = []
        for i in range(len(exist_list)):
            if i not in update_exist:
                exist_list[i].detect = False
                exist_list[i].point = [exist_list[i].point[0] + exist_list[i].vector[0],
                                       exist_list[i].point[1] + exist_list[i].vector[1]]
                exist_list[i].crush_dir, exist_list[i].crush_time = impact.impact(
                    exist_list[i].point, exist_list[i].vector)

                # 객체가 탐지 된지 5초 이상 지났거나, 가상좌표가 30 미터 이상 벌어지면 삭제한다.
                if time.time() - exist_list[i].timer > 5 or exist_list[i].point[0]**2 + exist_list[i].point[1]**2 > 900:
                    pass
                else:
                    temp_exist_list.append(exist_list[i])
            else:
                temp_exist_list.append(exist_list[i])
        exist_list = copy.deepcopy(temp_exist_list)

        for e in exist_list:
            if e.crush_time < min_crush_time:
                min_crush_time = e.crush_time
                c_dir = e.crush_dir

        if exist_list:
            t = datetime.datetime.now().time()
            t = str(t)
            f.write(t)
            f.write('\n')
        for e in exist_list:
            pluse_wirte = 'number : ' + str(e.number)
            f.write(pluse_wirte)
            f.write('\n')
            pluse_wirte = 'point : [' + str(round(e.point[0], 4)) + \
                ',' + str(round(e.point[1], 4)) + ']'
            f.write(pluse_wirte)
            f.write('\n')
            pluse_wirte = 'vector : [' + str(round(e.vector[0], 4)) + \
                ',' + str(round(e.vector[1], 4)) + ']'
            f.write(pluse_wirte)
            f.write('\n')

    # 전체 충돌을 가져오고, 가장 위험도가 높은 친구에 대해서 경고음이나 제동을 할 수 있도록 한다. (아님 그것을 리턴)
    return exists, c_dir, min_crush_time
