import os,sys

import cv2

dataDir = os.path.join(os.path.dirname(__file__), '../data')

for dirName in ('top_banner','bottom_banner','live_people','time','date'):
    os.makedirs(f"{dataDir}/{dirName}", exist_ok=True)

cap = cv2.VideoCapture(sys.argv[1])

keyframesFile = open(f'{dataDir}/1c_keyframes.txt')

for line in keyframesFile.readlines():
    frameIndex = int(line)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
    ret, frame = cap.read()
    if not ret:
        raise Exception('frame not found')
    
    # upper banner
    upperBanner = frame[255:290, 194:1200]
    cv2.imwrite(f'{dataDir}/top_banner/{frameIndex}.png', upperBanner)

    # live people
    livePeople = frame[900:942, 200:530]
    cv2.imwrite(f'{dataDir}/live_people/{frameIndex}.png', livePeople)

    # bottom banner
    bottomBanner = frame[967:1020, 200:800]
    cv2.imwrite(f'{dataDir}/bottom_banner/{frameIndex}.png', bottomBanner)

    # time
    time = frame[0:15, 1820:1880]
    cv2.imwrite(f'{dataDir}/time/{frameIndex}.png', time)

    # date
    date = frame[15:30, 1820:1880]
    cv2.imwrite(f'{dataDir}/date/{frameIndex}.png', date)

