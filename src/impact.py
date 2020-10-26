from math import *

# 현재포인트 x y  벡터 x y ~~
X_LENGTH = 0.75
Y_LENGTH = 1.5
def impact(pnt , vec):
    point_x, point_y = pnt[0],pnt[1]
    vec_x, vec_y = vec[0], vec[1]
    # 구역 할당
    impact_time = 100
    if abs(point_x) > 0.75 and point_y > 1.5:
        # 벡터 성분 분석
        if vec_y >= 0 or point_x * vec_x >= 0:
            impact_time = 100
        else :
            if point_x < 0:
                point_x = abs(point_x)
                vec_x = -vec_x
                # 벡터 각도 분석
            theta_v = atan(abs(vec_x) / abs(vec_y))
            theta_min = atan((point_x - 0.75) / point_y)
            theta_max = atan((point_x + 0.75) / (point_y - 0.75))
            theta_mid = atan((point_x - 0.75) / (point_y - 0.75))
            if theta_v >= theta_min and theta_v <= theta_max:
                if theta_v >= theta_mid:
                    impact_time = (point_y - 1.5) / abs(vec_y)
                else:
                    impact_time = (abs(point_x) - 0.75) / abs(vec_x)
                

    # 구역 할당
    elif abs(point_x) < 0.75 and point_y > 1.5:
        # 벡터 성분 분석
        if vec_y >= 0:
            impact_time = 100
        else :
            # 벡터 각도 분석
            theta_v = atan(abs(vec_x) / abs(vec_y))
            if vec_x <= 0 :
                if point_x >= 0:
                    theta_max = atan((point_x + 0.75) / point_y)
                    if theta_v > theta_max:
                        impact_time = 100
                    else:
                        impact_time = (point_y - 1.5) / abs(vec_y)
                        
                else:
                    theta_max = atan((0.75 - abs(point_x)) / point_y)
                    if theta_v > theta_max:
                        impact_time = 100
                    else:
                        impact_time = (point_y - 1.5) / abs(vec_y)
                        
            else:
                if point_x >=0:
                    theta_max = atan((point_x - 0.75) / point_y)
                    if theta_v > theta_max:
                        impact_time = 100
                    else:
                        impact_time = (point_y - 1.5) / abs(vec_y)
                        
                else:
                    theta_max = atan((abs(point_x) + 0.75) / point_y)
                    if theta_v > theta_max:
                        impact_time = 100
                    else:
                        impact_time = (point_y - 1.5) / abs(vec_y)
                        
        # 구역 할당
    elif point_y < 1.5:
            # 벡터 성분 분석
        if point_x * vec_x >= 0:
            impact_time = 100
        else :
                # 벡터 각도 분석
            theta_v = atan(abs(vec_y) / abs(vec_x))
            if vec_y >= 0:
                theta_max = atan((1.5 - point_y) / (abs(point_x) - 0.75))
                if theta_v > theta_max:
                    impact_time = 100
                else:
                    impact_time = (abs(point_x) - 0.75) / abs(vec_x)
                    
            else:
                theta_max = atan(point_y / (abs(point_x) - 0.75))
                if theta_v > theta_max:
                    impact_time = 100
                else:
                    impact_time = (abs(point_x) - 0.75) / abs(vec_x)
                
        
        # 경계선 포인트 확인
    elif point_y == 1.5 and abs(point_x) > 0.75:
        if vec_y > 0 or vec_x * point_x >= 0:
            impact_time = 100
        else:
            theta_v = atan(abs(vec_y) / abs(vec_x))
            theta_max = atan(1.5 / (abs(point_x) - 0.75))
            if theta_v > theta_max:
                impact_time = 100
            else:
                impact_time = (abs(point_x) - 0.75) / abs(vec_x)
                
        
        # 경계선 포인트 확인
    elif abs(point_x) == 0.75 and point_y > 1.5:
        if vec_y > 0 or vec_x * point_x >= 0:
            impact_time = 100
        else:
            theta_v = atan(abs(vec_x) / abs(vec_y))
            theta_max = atan(1.5 / (point_y - 1.5))
            if theta_v > theta_max:
                impact_time = 100
            else:
                impact_time = (point_y - 1.5) / abs(vec_y)
    
    dir = ''
    if point_x < (-1) * X_LENGTH :
        dir = 'LEFT'
    elif point_x > X_LENGTH :
        dir = 'RIGHT'
    else :
        dir = 'MIDDLE'

    return dir,impact_time

