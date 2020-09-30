#맵을 기준으로 매칭 로직을 실시한다.
from hungarian import hungarian_match 
import math

DISTANCE_SCALE = 10 
COLOR_SCALE = math.sqrt(3*pow(255,2)) #로그 스케일로 나타내는게 더 나을거같단 생각도 듭니다.

def matching(color_map, xy_map) :
    #SCALE 척도로 color_map 과 xy_map을 혼합한 뒤에 헝가리안 매칭을 시킨다.
    N = len(color_map)
    if N > 0 :
        M = len(color_map[0]) 
    else : 
        M = 0
    mathcing_map = [[0 for i in range(M)] for j in range(N)]
    for i in range(N) :
        for j in range(M) :
            #일단은 그냥 나누기 스케일로 배치, 두 값을 5:5 비율로 혼합
            mathcing_map[i][j] = xy_map[i][j] / DISTANCE_SCALE + color_map[i][j] / COLOR_SCALE
    match = hungarian_match(mathcing_map,max(N,M))
    
    # 관측점을 기준으로 생각.  거리기준 혹은 색 기준이 너무 다를경우 매칭이 되었어도 의심이 되는 경우. 아예 새로운 관측점으로 예상 될 경우 새로 만들어줘야할 것
    for i in match :
        past = match[i][0]
        now = match[i][1]
        # 가상의 지점과 매칭된 경우, 혹은 거리나 색이 너무 다른경우
        if xy_map[past][now] / DISTANCE_SCALE > 0.5 or color_map[past][now] / COLOR_SCALE > 0.5 or past >= N:
            # match의  past 가 -1 로 하면 알맞은 매칭점을 찾지 못한 형우
            match[i][0] = -1            

    return match