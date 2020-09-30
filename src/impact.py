import numpy as np
from math import *


# 현재포인트 x y  벡터 x y ~~

def impact(vec_array):
    # 킥보드 사이즈 (의견 나눈 뒤 조절 가능)
    # ndarray로 받아오는 형식 -> 각 행은 객체의 현재점 및 벡터 정보를 포함
    # sct_size_width = 1.5m
    # sct_size_height = 1.5m
    # 직전벡터사용
    impact_time_list = list()
    for vec in vec_array:
        point_x, point_y, vec_x, vec_y = vec[0], vec[1], vec[2], vec[3]
        # 구역 할당
        if abs(point_x) > 0.75 and point_y > 1.5:
            # 벡터 성분 분석
            if vec_y >= 0 or point_x * vec_x >= 0:
                impact_time_list.append(100)
                continue
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
                    impact_time_list.append(impact_time)
                    continue
                else:
                    impact_time = (abs(point_x) - 0.75) / abs(vec_x)
                    impact_time_list.append(impact_time)
                    continue
            else:
                impact_time_list.append(100)
                continue
        # 구역 할당
        elif abs(point_x) < 0.75 and point_y > 1.5:
            # 벡터 성분 분석
            if vec_y >= 0:
                impact_time_list.append(100)
                continue
            # 벡터 각도 분석
            theta_v = atan(abs(vec_x) / abs(vec_y))
            if vec_x <= 0 :
                if point_x >= 0:
                    theta_max = atan((point_x + 0.75) / point_y)
                    if theta_v > theta_max:
                        impact_time_list.append(100)
                        continue
                    else:
                        impact_time = (point_y - 1.5) / abs(vec_y)
                        impact_time_list.append(impact_time)
                        continue
                else:
                    theta_max = atan((0.75 - abs(point_x)) / point_y)
                    if theta_v > theta_max:
                        impact_time_list.append(100)
                        continue
                    else:
                        impact_time = (point_y - 1.5) / abs(vec_y)
                        impact_time_list.append(impact_time)
                        continue
            else:
                if point_x >=0:
                    theta_max = atan((point_x - 0.75) / point_y)
                    if theta_v > theta_max:
                        impact_time_list.append(100)
                        continue
                    else:
                        impact_time = (point_y - 1.5) / abs(vec_y)
                        impact_time_list.append(impact_time)
                        continue
                else:
                    theta_max = atan((abs(point_x) + 0.75) / point_y)
                    if theta_v > theta_max:
                        impact_time_list.append(100)
                        continue
                    else:
                        impact_time = (point_y - 1.5) / abs(vec_y)
                        impact_time_list.append(impact_time)
                        continue
        # 구역 할당
        elif point_y < 1.5:
            # 벡터 성분 분석
            if point_x * vec_x >= 0:
                impact_time_list.append(100)
                continue

            # 벡터 각도 분석
            theta_v = atan(abs(vec_y) / abs(vec_x))
            if vec_y >= 0:
                theta_max = atan((1.5 - point_y) / (abs(point_x) - 0.75))
                if theta_v > theta_max:
                    impact_time_list.append(100)
                    continue
                else:
                    impact_time = (abs(point_x) - 0.75) / abs(vec_x)
                    impact_time_list.append(impact_time)
                    continue
            else:
                theta_max = atan(point_y / (abs(point_x) - 0.75))
                if theta_v > theta_max:
                    impact_time_list.append(100)
                    continue
                else:
                    impact_time = (abs(point_x) - 0.75) / abs(vec_x)
                    impact_time_list.append(impact_time)
                    continue
        # 경계선 포인트 확인
        elif point_y == 1.5 and abs(point_x) > 0.75:
            if vec_y > 0 or vec_x * point_x >= 0:
                impact_time_list.append(100)
                continue
            else:
                theta_v = atan(abs(vec_y) / abs(vec_x))
                theta_max = atan(1.5 / (abs(point_x) - 0.75))
                if theta_v > theta_max:
                    impact_time_list.append(100)
                    continue
                else:
                    impact_time = (abs(point_x) - 0.75) / abs(vec_x)
                    impact_time_list.append(impact_time)
                    continue
        # 경계선 포인트 확인
        elif abs(point_x) == 0.75 and point_y > 1.5:
            if vec_y > 0 or vec_x * point_x >= 0:
                impact_time_list.append(100)
                continue
            else:
                theta_v = atan(abs(vec_x) / abs(vec_y))
                theta_max = atan(1.5 / (point_y - 1.5))
                if theta_v > theta_max:
                    impact_time_list.append(100)
                    continue
                else:
                    impact_time = (point_y - 1.5) / abs(vec_y)
                    impact_time_list.append(impact_time)
                    continue
        # 충돌 박스 내부 확인
        else:
            # 충돌 박스 내부일 경우 충돌 0초(즉시 충돌)와 인덱스 반환
            #is_impact = [0,np.where(vec_array == vec)[0][0]]
            #return is_impact
            impact_time_list.append(0)
            continue

    # 칼만필터 예측벡터 사용
    # 가장 작은 시간 및 객체 index 반환 (list)
    min_time = min(impact_time_list)
    min_index = impact_time_list.index(min_time)
    is_impact = [min_time, min_index]
    print(impact_time_list)
    return is_impact

