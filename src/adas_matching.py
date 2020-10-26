# 맵을 기준으로 매칭 로직을 실시한다.
from hungarian import hungarian_match
import math
INF = 999999999
COLOR_SCALE = math.sqrt(3*pow(255, 2))  # 로그 스케일로 나타내는게 더 나을거같단 생각도 듭니다.

# 정방행렬임


def matching(color_map, xy_map):
    # SCALE 척도로 color_map 과 xy_map을 혼합한 뒤에 헝가리안 매칭을 시킨다.
    N = len(color_map)
    mathcing_map = [[0 for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            # 색이 굉장히 비슷할 경우에는, 거리를 더욱 가깝다고 판단시켜 매칭시켜본다
            if color_map[i][j] < 10 and xy_map[i][j] != INF:
                mathcing_map[i][j] = xy_map[i][j] * 0.5
            else:
                mathcing_map[i][j] = xy_map[i][j]
    match = hungarian_match(mathcing_map, N)
    # 경험적으로 재시도
    # 관측점을 기준으로 생각.  거리기준 혹은 색 기준이 너무 다를경우 매칭이 되었어도 의심이 되는 경우. 아예 새로운 관측점으로 예상 될 경우 새로 만들어줘야할 것

    for i in range(len(match)):
        past = match[i][0]
        now = match[i][1]
        # 가상의 지점과 매칭된 경우, 가상지점으로 해줌
        if mathcing_map[past][now] == INF:
            # match의  past 가 -1 로 하면 알맞은 매칭점을 찾지 못한 형우
            match[i][0] = -1

    return match
