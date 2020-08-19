import cv2
import numpy as np

# Input parameter from GML tool
cam_mtx=np.array([[556.375,0,330.334],[0,556.416,255.302],[0,0,1]]) # Camera matrix
dist=np.array([-0.335978,0.133403,0.000953,0.000789]) # Distortion parameter

# Find image
img=cv2.imread('sample_img.jpg')
h,w=img.shape[:2]

# Improve camera matrix
new_cam_mtx, roi=cv2.getOptimalNewCameraMatrix(cam_mtx,dist,(w,h),1,(w,h))
#roi는 region of interest로 이미지의 주 관심 영역을 의미

# Calibration
unDist = cv2.undistort(img,cam_mtx,dist,None,new_cam_mtx)
cv2.imwrite('new_image.png',unDist)
