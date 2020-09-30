#Calibration & Roi's Color 

#pixel 좌표계를 현실의 xy 좌표계로 변환해줍니다.  인자 : left- pixel x , left- pixel y ~~~
def real_coordinate(p1,p2) :
    l_px,l_py = p1
    r_px,r_py = p2
    fx = 315.51*2  # focal length x
    fy = 312.72*2  # focal length y
    cx = 335.01*2  # Principal point x
    cy = 229.88*2  # Principal point y
    h = 1.25 # 카메라 높이 h

    #왼쪽 아래점 변환
    u1=(l_px - cx) / fx
    v1=(l_py - cy) / fy
    l_ry = h/v1 #left- real y
    l_rx = u1 * l_ry

    #오른쪽 아래점 변환
    u1=(r_px - cx) / fx
    v1=(r_py - cy) / fy
    r_ry = h/v1
    r_rx = u1 * r_ry

    #중앙점 반환
    m_rx = (r_rx + l_rx)/2
    m_ry = ((r_ry + l_ry)/2)*-1

    return [m_rx, m_ry]


#ROI 영역의 색을 구해줍니다. 현재는 평균값 사용
def determine_color(roi_color) :
    color = [0,0,0]
    n = len(roi_color)
    for r,g,b in roi_color :  
        color = [color[0]+r, color[1]+g , color[2]+b]
    color = [color[0]//n , color[1]//n, color[2]//n]
    return color    
