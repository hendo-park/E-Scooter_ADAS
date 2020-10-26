from math import *

# 현재포인트 x y  벡터 x y ~~
# 킥보드 크기로 가정하는 충돌 임계 박스 크기
X_LENGTH = 0.75
Y_LENGTH = 1.5

def get_angle(v1, v2):

    return angle

def impact(pnt, vec):
    point_x, point_y = pnt[0], pnt[1]
    vec_x, vec_y = vec[0], vec[1]
    impact_time = 100
    # 전방에서 충돌
    if abs(point_x) <= X_LENGTH:
        if point_y <= Y_LENGTH: # 객체 좌표가 임계 박스 안에 있는 경우 즉시 충돌 반환
            return 'IMPACT_NOW', 0
        if vec_y < 0: # vec_y가 0 이상이면 충돌하지 않음
            if point_x > 0: # y축 기준 벡터 대칭
                point_x = -point_x
                vec_x = -vec_x
            # 내적을 통한 각도 계산
            std_vec = (1, 0) # 각도 비교를 위한 기준 벡터
            max_vec = (-X_LENGTH - point_x, Y_LENGTH - point_y)
            min_vec = (X_LENGTH - point_x, Y_LENGTH - point_y)
            max_angle = get_angle(max_vec, std_vec)
            min_angle = get_angle(min_vec, std_vec)
            target_angle = get_angle(vec, std_vec)
            if min_angle <= target_angle <= max_angle:
                impact_time = (Y_LENGTH - point_y) / vec_y # y 기준 충돌시간
                return 'MIDDLE IMPACT', impact_time
    # 좌, 우측 충돌 확인
    elif abs(point_x) > X_LENGTH:
        direction = 'LEFT IMPACT'
        # 사이드 하단
        if point_y < Y_LENGTH:
            if (point_x * vec_x) < 0:
                if point_x > 0:
                    direction = 'RIGHT IMPACT'
                    point_x = -point_x
                    vec_x = -vec_x
                std_vec = (0, -1)
                max_vec = (-X_LENGTH - point_x, Y_LENGTH - point_y)
                min_vec = (-X_LENGTH - point_x, -point_y)
                max_angle = get_angle(max_vec, std_vec)
                min_angle = get_angle(min_vec, std_vec)
                target_angle = get_angle(vec, std_vec)
                if min_angle <= target_angle <= max_angle:
                    impact_time = (-X_LENGTH - point_x) / vec_x
                    return direction, impact_time
        # 사이드 상단
        else:
            if vec_y < 0:
                if point_x > 0:
                    direction = 'RIGHT IMPACT'
                    point_x = -point_x
                    vec_x = -vec_x
                # 내적을 통한 각도 계산
                std_vec = (1,0)
                max_vec = (X_LENGTH - point_x, Y_LENGTH - point_y)
                mid_vec = (-X_LENGTH - point_x, Y_LENGTH - point_y)
                min_vec = (-X_LENGTH - point_x, -point_y)
                max_angle = get_angle(max_vec, std_vec)
                mid_angle = get_angle(mid_vec, std_vec)
                min_angle = get_angle(min_vec, std_vec)
                target_angle = get_angle(vec, std_vec)
                if min_angle <= target_angle <= mid_angle:
                    impact_time = (-X_LENGTH - point_x) / vec_x
                    return direction, impact_time
                elif mid_angle < target_angle <= max_angle:
                    impact_time = (Y_LENGTH - point_y) / vec_y
                    return direction, impact_time
    # 위에서 종료되지 않으면 충돌하지 않는 경우
    return 'NOT IMPACT', impact_time