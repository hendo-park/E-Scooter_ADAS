import bangul_matching
import math
from similarity import cosine_map 
import time
import collections as col

class detect_object :
    def __init__(self,label,number,value) :
        #검출 객체 종류
        self.label = label
        self.number = number
        #상태값 초기화 
        self.point = value['point'] #현재 좌표값
        self.color = value['color'] # 색
        self.gridbox = value['gridbox']
        self.timer = time.time() #감지된 시간
        self.detect = True
        self.path = []
        self.path.append([self.point,self.timer])
        self.vector = 0

    def update(self, value ) :
        self.point = value['point']
        self.timer = time.time()
        self.path.append([self.point,self.timer])
        self.color = value['color'] 
        self.gridbox = value['gridbox']
        self.detect = True
    



    # 확장형 칼만 필터 예측 및 수정 부분    
    # def ekf_predict(self) :
    # def ekf_correct(self) :



def track(exists,values,detect_list) :
    for object_label in detect_list :
        exist_list = exists[object_label] #얘는 class 
        value_list = values[object_label] #얘는 딕셔너리 형태
        LEN_EXIST = len(exist_list)
        LEN_NEW = len(value_list)

        #번호 지정
        deq = col.deque()
        numberlist = [False for i in range(11)]
        for i in range(LEN_EXIST) :
            numberlist[exist_list.number] = True
        for i in range(1,11) :
            if numberlist[i] == False :
                deq.append(i)



        #color 맵 구성        
        exist_color = []
        for i in range(LEN_EXIST) :
            exist_color.append(exist_list[i].color)

        new_color = []
        for i in range(LEN_NEW) : 
            new_color.append(value_list[i]['color'])

        color_map = cosine_map(exist_color, new_color)

        #color 에 의한 헝가리안 매칭, 거리가 일정 수준 이하인 매칭의 경우 따로 빼줄 수 있도록 한다.


        #xy coordinate 맵 구성

        #존재 지점의 경우 벡터를 기반으로 갱신한다 이때, 화면을 벗어났을 것으로 예상되는 객체는 삭제할 수 있도록 한다.
        exist_point = []
        for i in range(LEN_EXIST) :
            exist_point.append(exist_list.point) #일단 현재 지점만 가지고 해보자

        #측정지점의 경우 그대로 사용한다
        new_point = []
        for i in range(LEN_NEW) : 
            new_point.append(value_list[i]['point'])


        xy_map = cosine_map(exist_point, new_point)



        #매칭을 실행한다
        update_exist = []
        match = bangul_matching.matching(color_map,xy_map)
        for past,now in match :
            if past == -1 :
                #새로운 객체를 생성한다
                exist_list.append(detect_object(object_label,deq.popleft(),value_list[now]))               
            else :
                #존재하던 객체를 갱신한다
                exist_list[past].update(value_list[now])
                update_exist.append(past)


        #현재 검출되지 않은 객체의 경우 실존하지 않음은 알려줘야한다 (왜냐하면 그걸로 멈출순 없으니까)
        for i in range(LEN_EXIST) :
            if i not in update_exist:
                exist_list[i].detect = False

        

    return exists

    

