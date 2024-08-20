import os,sys

import cv2

dataDir = os.path.join(os.path.dirname(__file__), '../data')

cap = cv2.VideoCapture(sys.argv[1])

# 随意取一帧用来判断图片
cap.set(cv2.CAP_PROP_POS_FRAMES, 70011)

ret, frame = cap.read()

cv2.imwrite(f"{dataDir}/1a_random_frame.png", frame)


