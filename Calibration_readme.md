#Process of camera calibration

##Step 1. Extract parameter
GML camera calibration tool을 사용하여 카메라 렌즈 왜곡 보정 계수를 구한다.
툴을 이용하기 위해 정해진 흑백 격자무늬 패턴을 사용해야 하는데, 같은 폴더 참조 바람.
패턴을 출력해 여러 각도, 거리에서 사진을 촬영한다.
패턴 개수(n by n)와 패턴의 크기(each of square size)를 툴에 입력 후 패턴 격자의 교점들을 찾는다.
마지막으로 툴에서 calibration 수행을 통해 focal length, principal point등 주점과 distortion parameter, camera matrix를 추출할 수 있다.
마지막으로 Calibrate를 눌러 이미지를 각각 이미지를 수정할 수 있으나 OpenCV의 undistort 메소드를 사용해 직접 보정할 수도 있다.

##Step 2. Use OpenCV for calibration
폴더 내에 첨부된 sample 코드를 적절히 변형하여 사용한다.
카메라 매트릭스, 왜곡보정 계수는 GML 툴에서 나온 값을 활용한다.
