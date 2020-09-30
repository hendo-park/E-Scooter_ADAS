# 헝가리안 알고리즘
import konig
import copy
import collections as col
def hungarian_match(Map, n) :
    #모든 행에 대해서, 그 행의 각 원소에 그 행에서 가장 작은 값을 뺀다.
    for i in range(0,n) :
        min_len = 99999999
        for j in range(0,n) :
            min_len = min(Map[i][j], min_len)
        for j in range(0,n) :
            Map[i][j] = Map[i][j] - min_len

    #모든 열에 대해서, 그 열의 각 원소에 그 열에서 가장 작은 값을 뺀다.
    for i in range(0,n) :
        min_len = 99999999
        for j in range(0,n) :
            min_len = min(Map[j][i], min_len)
        for j in range(0,n) :
            Map[j][i] = Map[j][i] - min_len

    #행과 열을 n개보다 적게 뽑아서, 행렬의 모든 0의 값을 갖는 원소를 덮는 방법이 없을 때 까지 아래를 반복한다.
    while True :
        Map2 = copy.deepcopy(Map) #기존의 맵은 konig  알고리즘 수행중에는 손항되어선 안됩니다.
        Except_X,Except_Y,cnt = konig.konig(Map2,n) #konig알고리즘을 통해 커버할 열과 행을 정합니다
        if cnt == n :
            break
        #뽑힌 곳을 제외하고 가장 작은 수를 구합니다
        min_len = 99999999
        for i in range(n) :
            for j in range(n) :
                if Except_X.count(i) == 0 and Except_Y.count(j) == 0 :
                    min_len = min(min_len, Map[i][j])
        # Except_X 에 속하지 않는 행에 대해서만 최소 비용 뺄샘을 진행합니다
        for i in range(n) :
            if i not in Except_X :
                for j in range(n) :
                    Map[i][j] = Map[i][j] - min_len
        # Except_Y에 속하는 열에 대해서 최소 비용 덧샘을 진행합니다.
        for i in Except_Y :
            for j in range(n) :
                Map[j][i] = Map[j][i] + min_len
        
    #과정이 끝나면 DFS로 배치를 시작합니다.
    # deq의 원소는 현재까지 매칭리스트 visit과, 현재 행으로 이루어집니다.
    visit = [-1 for i in range(n)]
    deq = col.deque()
    for i in range(n) :
        if Map[0][i] == 0 :
            ivisit = copy.deepcopy(visit)
            ivisit[i] = 0
            deq.append([1, ivisit])
    while len(deq) != 0 :
        x,visit = deq.pop()
        if x == n :
            break
        for i in range(n) :
            if visit[i] == -1 and Map[x][i] == 0 :
                ivisit = copy.deepcopy(visit)
                ivisit[i] = x
                deq.append([x+1, ivisit])

    #visit에 매칭 리스트가 적혀저있습니다. (번지 수 : 열 - 번지 값 : 행  , 거리까지 내보내줬으면 하는데)
    result = []
    for i in range(n) :
        result.append([visit[i], i])
    return result