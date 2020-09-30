import math
INF = 999999999


#p1 = (1,2,3)   p2 = (3,4,5)      p1(1,2)  p2(1,3)
def cos_similarity(p1, p2) :
    distance = 0
    N = len(p1)
    for i in range(N) :
        distance = distance + pow(p1[i] - p2[i],2)
    return math.sqrt(distance)


def cosine_map(l1, l2) :
    N = len(l1)
    M = len(l2)
    K = max(N,M)
    # 예측점과 측정점 중 더 개수가 많은 값을 중심으로 정방 행렬을 만들어야하며, 길이가 다른 경우 가상의 거리를 만들어서 사용한다.
    distance = [[INF for i in range(K)] for j in range(K)] 

    for i in range(0,N) :
        for j in range(0,M) :
            distance[i][j] = cos_similarity(l1[i],l2[j])
    return distance