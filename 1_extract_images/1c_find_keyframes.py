import os, sys

import cv2

dataDir = os.path.join(os.path.dirname(__file__), "../data")

# 开始刷新大约在 5min, 2024-08-19T21:58+08:00
startFrameIndex = 5 * 60 * 60

refreshButton = cv2.imread(f"{dataDir}/1b_refresh_icon.png")
if refreshButton is None:
    print("refresh button not found")
    sys.exit(1)

cap = cv2.VideoCapture(sys.argv[1])

cap.set(cv2.CAP_PROP_POS_FRAMES, startFrameIndex)

f = open(f"{dataDir}/1c_keyframes.txt", "a+")

lastSum = 0
frameIndex = startFrameIndex
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # if frameIndex > startFrameIndex + 4 * 60 * 60:
    #     print("early stop")
    #     break
    # if frameIndex % (60 * 60) == 0:
    #     print(frameIndex // (60 * 60))

    # 获取刷新按钮区域
    refresh = frame[68:88, 62:82]

    # 获取差值
    diff = cv2.absdiff(refreshButton, refresh)
    sums = cv2.sumElems(diff)
    sumAll = sums[0] + sums[1] + sums[2]

    if sumAll > 2000 and lastSum < 2000:
        print("keyframe found at", frameIndex)
        f.write(str(frameIndex) + "\n")
        f.flush()
        # 跳50s
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex + 50 * 60)
        frameIndex = frameIndex + 50 * 60

    lastSum = sumAll

    frameIndex += 1
