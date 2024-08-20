
import os,sys

import cv2

dataDir = os.path.join(os.path.dirname(__file__), '../data')

full = cv2.imread(f"{dataDir}/1a_random_frame.png")

# refresh button
refresh = full[68:88, 62:82]

cv2.imwrite(f'{dataDir}/1b_refresh_icon.png', refresh)

# time
time = full[0:15, 1820:1880]

cv2.imwrite(f'{dataDir}/1b_time.png', time)

# date
date = full[15:30, 1820:1880]

cv2.imwrite(f'{dataDir}/1b_date.png', date)

# upper banner
upperBanner = full[255:290, 194:1200]

cv2.imwrite(f'{dataDir}/1b_upper_banner.png', upperBanner)

# live people
livePeople = full[900:942, 200:530]

cv2.imwrite(f'{dataDir}/1b_live_people.png', livePeople)

# bottom banner
bottomBanner = full[967:1020, 200:800]

cv2.imwrite(f'{dataDir}/1b_bottom_banner.png', bottomBanner)
