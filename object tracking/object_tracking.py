import numpy as np
import copy

Get_Out_List = [[]]

def Matching_DFS(Now_N, Distance_List, Matching_N, Matching_List) : #mesured 기준으로 진행하세요 (y열 기준 진행)
   if Now_N == Matching_N :
       
       global Get_Out_List
       Get_Out_List = copy.deepcopy(Matching_List)
       return 
   else :
        for i in range (0,Matching_N) :
         if Distance_List[Now_N][i]==0 :
             flag=0
             for j in range (0,Now_N) :
                 if Matching_List[j][1]==i :
                     flag=1
                     break
             if flag== 0 :
                Matching_List.append([Now_N,i])
                Matching_DFS(Now_N+1,Distance_List,Matching_N,Matching_List)
                Matching_List.pop()

            

def Konig_Algorithm(Distance_List, Matching_N):
    
    Except_X=[]
    Except_Y=[]
    Complete_Line = 0
    while True :         
        XY_List=[[0 for i in range(0,Matching_N)] for j in range (0,2)]
        for i in range(0,Matching_N) :
             XY_List[0][i]=Distance_List[i].count(0)
        flag=0
        for i in range(0,Matching_N) :
            for j in range(0,Matching_N) :
                if Distance_List[j][i]== 0 :
                    XY_List[1][i]=XY_List[1][i]+1
                    flag=1
        if flag==0 :
            break
        Max_XY=0
        Max_Point=0
        Max_Zero=0
        for i in range(0,2) :
            for j in range(0,Matching_N) :
              if Max_Zero<XY_List[i][j] :
                Max_Zero=XY_List[i][j]
                Max_Point=j
                Max_XY=i
        if Max_XY==0 :
            for i in range(0,Matching_N) :
                if Distance_List[Max_Point][i]==0 :
                    Distance_List[Max_Point][i]=-1
            Except_X.append(Max_Point)     
            Complete_Line=Complete_Line+1
   
        elif Max_XY==1 :
            for i in range(0,Matching_N) :
                if Distance_List[i][Max_Point]==0 :
                    Distance_List[i][Max_Point]=-1
            Except_Y.append(Max_Point)  
            Complete_Line=Complete_Line+1

    return Except_X,Except_Y,Complete_Line


#List의 경우  x좌표, y좌표로 구성
def Hungarian_Algorithm(Predict_Point_List, Measured_Point_List) :   
    n=len(Predict_Point_List)
    m=len(Measured_Point_List)
    Matching_N = max(n,m)
    Min_Length=99999999
    Distance_List=[[0 for i in range(Matching_N)] for j in range(Matching_N)]

    for i in range(0,n) :
        for j in range(0,m) :
            Distance_List[i][j]=(Predict_Point_List[i][0]-Measured_Point_List[j][0])*(Predict_Point_List[i][0]-Measured_Point_List[j][0]) + (Predict_Point_List[i][1]-Measured_Point_List[j][1])*(Predict_Point_List[i][1]-Measured_Point_List[j][1])

    if n>m :
        for i in range(m,n) :
            for j in range(0,n) :
                Distance_List[j][i]=10
    elif n<m :
        for i in range(n,m) :
            for j in range(0,n) :
                Distance_List[i][j]=10


    for i in range(0,Matching_N) :
        Min_Length=99999999
        for j in range(0,Matching_N) :
            Min_Length = min(Min_Length,Distance_List[i][j])
        for j in range(0,Matching_N) :
            Distance_List[i][j]= Distance_List[i][j]-Min_Length
    
    for i in range(0,Matching_N) :
        Min_Length=99999999
        for j in range(0,Matching_N) :
            Min_Length = min(Min_Length,Distance_List[j][i])
        for j in range(0,Matching_N) :
            Distance_List[j][i]= Distance_List[j][i]-Min_Length
    
    Distance_List2=copy.deepcopy(Distance_List)  
    Except_X,Except_Y,Complete_Line =  Konig_Algorithm(Distance_List2,Matching_N)
    
    while Complete_Line != Matching_N :
        Min_Length=99999999
        for i in range(0,Matching_N) :
             for j in range(0,Matching_N) :
                    if Except_X.count(i)==0 and Except_Y.count(j)==0 :
                           Min_Length = min(Min_Length,Distance_List[i][j])
        for i in range(0,Matching_N) :
             for j in range(0,Matching_N) :
                    if Except_X.count(i)==0 and Except_Y.count(j)==0 :
                           Distance_List[i][j] = Distance_List[i][j]-Min_Length
        for i in range(0,len(Except_X)) :
             for j in range(0,len(Except_Y)) :
                 Distance_List[Except_X[i]][Except_Y[j]]=Distance_List[Except_X[i]][Except_Y[j]] + Min_Length
        Distance_List2=copy.deepcopy(Distance_List)  
        Except_X,Except_Y,Complete_Line =Konig_Algorithm(Distance_List2,Matching_N)     
    
  
    Matching_DFS(0,Distance_List,Matching_N,[])
    global Get_Out_List
    #m까지만 반환시켜주면 소멸된 애들까지 체크 가능함. 데려가서 현재 사람들 리스트 재구성할것
    return Get_Out_List





class human:
    def __init__(self,llx,lly,lrx,lry):
        #좌표값 받아와서 변환하는것은 여기서 해주자
        self.L_Ly=0
        self.L_Lx=0
        self.L_Ry=0
        self.L_Rx=0
        self.Now_Mid_X=0
        self.Now_Mid_Y=0
        self.Change_Real_Parameter(llx,lly,lrx,lry)

        #임시로 주는 값
        self.Now_Mid_X=(llx+lrx)/2
        self.Now_Mid_Y=(lly+lry)/2
        #임시로 주는 값 끝

        self.Past_Mid_X= self.Now_Mid_X
        self.Past_Mid_Y= self.Now_Mid_Y
        self.X_Vector = 0
        self.Y_Vector = 0
        self.Crush_Time = 9999999
        self.P_Number = 0
        self.Kalman_Gain = np.array([[0,0,0,0],[0,0,0,0] , [0,0,0,100] , [0,0,100,0] ]) #초기값 배열
        self.Kalman_P_now = np.array([[0,0,0,0],[0,0,0,0] , [0,0,0,100] , [0,0,100,0] ]) #초기값 배열     
        self.Kalman_P_predict = np.array([[0,0,0,0],[0,0,0,0] , [0,0,0,100] , [0,0,100,0] ])
        self.Predict_X=0
        self.Predict_Y=0
        self.Kalman_z = np.array([[self.Now_Mid_X],[self.Now_Mid_Y]])
        self.Kalman_x_now = np.array([[self.Now_Mid_X],[self.X_Vector],[self.Now_Mid_Y],[self.Y_Vector]])
        self.Kalman_x_predict = np.array([[self.Now_Mid_X],[self.X_Vector],[self.Now_Mid_Y],[self.Y_Vector]])

    def KalmanFilter_Predict(self) :
        A=np.array([[1,0.2,0,0],[0,1,0,0] , [0,0,1,0.2] , [0,0,0,1] ]) #상태벡터 도출 벡터
        Q=np.array([[1,0,0,0],[0,1,0,0] , [0,0,1,0] , [0,0,0,1] ])

        self.Kalman_x_predict= A @ self.Kalman_x_now
        self.Kalman_P_predict = A @ self.Kalman_P_now @ np.transpose(A) + Q
        return [self.Kalman_x_predict[0][0],self.Kalman_x_predict[2][0]]

    def KalmanFilter_Correct(self,correct_z_x, correct_z_y) :
         H=np.array([[1,0,0,0],[0,1,0,0]])
         R=np.array([[50,0],[0,50]])
         I=np.array([[1,0,0,0],[0,1,0,0] , [0,0,1,0] , [0,0,0,1] ])
         self.Kalman_z = np.array([[correct_z_x],[correct_z_y]])
         self.Kalman_Gain =( self.Kalman_P_predict @ np.transpose(H) ) @ np.linalg.inv(H @ self.Kalman_P_predict @ np.transpose(H) + R )
         self.Kalman_x_now = self.Kalman_x_predict + self.Kalman_Gain @ (self.Kalman_z - H @ self.Kalman_x_predict)
         self.Kalman_P_now = (I- self.Kalman_Gain @ H ) @ self.Kalman_P_predict



    def Change_Real_Parameter(self, llx,lly,lrx,lry) :
        fx = 978.732  # focal length x
        fy = 987.730  # focal length y
        cx = 939.305  # Principal point x
        cy = 533.219  # Principal point y
        h = 1.1  # 카메라 높이 M

        #왼쪽 아래점 변환
        u1=(llx - cx) / fx
        v1=(lly - cy) / fy
        self.L_Ly = h/v1
        self.L_Lx = u1 * self.L_Ly

        #오른쪽 아래점 변환
        u1=(lrx - cx) / fx
        v1=(lry - cy) / fy
        self.L_Ry = h/v1
        self.L_Rx = u1 * self.L_Ry

        #중앙점 반환
        self.Now_Mid_X = (self.L_Lx + self.L_Rx)/2
        self.Now_Mid_Y = (self.L_Ly + self.L_Ry)/2



    def Set_PastPoint(self,nx,ny,t) :
        self.Past_Mid_X=self.Now_Mid_X
        self.Past_Mid_Y=self.Now_Mid_Y
        self.Now_Mid_X = nx
        self.Now_Mid_Y = ny
        self.X_Vector=(self.Now_Mid_X - self.Past_Mid_X) / t
        self.Y_Vector=(self.Now_Mid_Y - self.Past_Mid_Y) / t




    def Set_CrushTime(self) :
        #0으로 나누는거 방지해줘야함, 일단은 중앙점 위주로 판단

        X_Crush_Time = [0,0] # 0 번지 충돌 최소 시간, 1번지 충돌 벗어나는 시간
        Y_Crush_Time = [0,0] # 0 번지 충돌 최소 시간, 1번지 충돌 벗어나는 시간
        
        #X_Crush_Time 처리 좌우 합 1.5m안쪽으로 판정
        if self.Now_Mid_X >=0.75 : # x 0.75 바깥쪽에서 움직이는 경우
            X_Crush_Time[0] = (-1) * ((self.Now_Mid_X - 0.75) / self.X_Vector)
            X_Crush_Time[1] = (-1) * ((self.Now_Mid_X + 0.75) / self.X_Vector)
        elif self.Now_Mid_X <=-0.75 : # x -0.75 바깥쪽에서 움직이는 경우
            X_Crush_Time[0] = (-1) * ((self.Now_Mid_X + 0.75) / self.X_Vector)
            X_Crush_Time[1] = (-1) * ((self.Now_Mid_X - 0.75) / self.X_Vector)
            
        else : # x 가 충돌 지역 안쪽일 경우
            X_Crush_Time[0] = 0
            if self.X_Vector >=0 :
                X_Crush_Time[1]= (0.75- self.Now_Mid_X) / self.X_Vector
            else :
                X_Crush_Time[1]= (-0.75- self.Now_Mid_X) / self.X_Vector
        if X_Cruch_Time[0] < 0 : #시간이 음수이면 충돌 안함
            X_Crush_Time[0] = 9999999
            X_Crush_Time[1] = 9999999
        
        #Y_Crush_Time 처리 1m 안쪽으로 설정
        if self.Now_Mid_Y >=1 : # Y 1 바깥쪽에서 움직이는 경우
            Y_Crush_Time[0] = (-1) * ((self.Now_Mid_Y - 1) / self.Y_Vector)
            Y_Crush_Time[1] = (-1) * ((self.Now_Mid_Y + 0) / self.Y_Vector)
        else : # Y 가 충돌 지역 안쪽일 경우
            Y_Crush_Time[0] = 0
            if self.Y_Vector >=0 :
                Y_Crush_Time[1]= (1- self.Now_Mid_Y) / self.Y_Vector
            else :
                Y_Crush_Time[1]= (-1 * self.Now_Mid_Y) / self.Y_Vector
        if Y_Cruch_Time[0] < 0 : #시간이 음수이면 충돌 안함
            Y_Crush_Time[0] = 9999999
            Y_Crush_Time[1] = 9999999
        
        # 둘 사이의 충돌 시간 겹치는 시간을 통해서 실제 충돌 시간 판정
        Fast_Time = max(X_Crush_Time[0],Y_Crush_Time[0])
        Late_Time = min(X_Crush_Time[1],Y_Crush_Time[1])
        if Fast_Time <= Late_Time :
            self.Crush_Time = Fast_Time
        else :
            self.Crush_Time = 9999999






# 사람이 여러명이라 치자
z=[]
p=[]
k= human(0,0,0,0)
z.append(k)
k = human(0,0,0,8)
z.append(k)
#새로운 값은 이거라고 쳐보자
k= human(0,0,2,2)
p.append(k)
k= human(0,0,2,10)
p.append(k)

predicts=[]
predicts.append(z[0].KalmanFilter_Predict())
predicts.append(z[1].KalmanFilter_Predict())

corrects=[]
corrects.append([p[0].Now_Mid_X , p[0].Now_Mid_Y])
corrects.append([p[1].Now_Mid_X , p[1].Now_Mid_Y])

correct_list = Hungarian_Algorithm(predicts,corrects)


for i in range (0,2) :
    z[i].Set_PastPoint(corrects[correct_list[i][1]][0],corrects[correct_list[i][1]][1],0.2)
    z[i].KalmanFilter_Correct(corrects[correct_list[i][1]][0],corrects[correct_list[i][1]][1])


p.pop()
p.pop()

#새로운 값은 이거라고 쳐보자
k= human(0,0,6,6)
p.append(k)
k= human(0,0,4,12)
p.append(k)

predicts=[]
predicts.append(z[0].KalmanFilter_Predict())
predicts.append(z[1].KalmanFilter_Predict())

corrects=[]
corrects.append([p[0].Now_Mid_X , p[0].Now_Mid_Y])
corrects.append([p[1].Now_Mid_X , p[1].Now_Mid_Y])

correct_list = Hungarian_Algorithm(predicts,corrects)

for i in range (0,2) :
    z[i].Set_PastPoint(corrects[correct_list[i][1]][0],corrects[correct_list[i][1]][1],0.2)
    z[i].KalmanFilter_Correct(corrects[correct_list[i][1]][0],corrects[correct_list[i][1]][1])
    