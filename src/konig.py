global adj 
global visited,CoverA,CoverB
global match,matchx
def dfs(cur) :
    global adj 
    global visited,CoverA,CoverB    
    global match,matchx
    visited[cur] =True
    for to in adj[cur] :
        if matchx[to] == -1 or  (visited[matchx[to]] == False  and dfs(matchx[to])==True) :
            matchx[to]=cur
            match[cur]= to
            return True
    return False

def bfs(now) :
    global adj 
    global visited,CoverA,CoverB    
    global match,matchx
    deq = col.deque()
    deq.append(now)
    visited[now]= True
    CoverA[now] = False
    while len(deq)!=0 :
        cur = deq.popleft()
        CoverA[cur] = False
        for to in adj[cur] :
            if visited[matchx[to]]==True :
                continue
            if match[cur]!= to and matchx[to]!= -1 :
                deq.append(matchx[to])
                visited[matchx[to]]==True
                CoverB[to]= True
    return

#쾨니그 정리, 이분매칭을 사용한다.
def konig(Map,n):
    global adj 
    global visited,CoverA,CoverB
    global match,matchx
    adj =  [[] for i in range(n)]
    match = [-1 for i in range(n)]
    matchx = [-1 for i in range(n)]
    CoverA = [True for i in range(n)]
    CoverB = [False for i in range(n)]
    for i in range(n) :
        for j in range(n) :
            if Map[i][j]==0 :
                adj[i].append(j)
    ans = 0
    #DFS로 매칭점을 찾는다
    for i in range(n) :
        visited = [False for j in range(n)]
        flag = dfs(i)
        if flag == True :
            ans = ans+1

    #경로찾기, BFS를 사용한다. match가 -1이면 쓰이지 않은 라인 = bfs
    visited = [False for j in range(n)]
    for i in range(n) :
        if visited[i] == False and match[i] == -1 :
            bfs(i)

    #커버 하기 위해 지워진 행
    Except_X = []
    #커버 하기 위해 지워진 열
    Except_Y = []
    for i in range(n) :
        if CoverA[i] == True :
            Except_X.append(i)
        if CoverB[i] == True :
            Except_Y.append(i)

    #커버 하기 위해 지워진 행, 열들과 사용된 총 개수를 반환한다.
    return Except_X,Except_Y,ans
