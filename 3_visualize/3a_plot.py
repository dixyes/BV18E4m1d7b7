from collections import OrderedDict
import os,sys
import datetime
from typing import Optional

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

dataDir = os.path.join(os.path.dirname(__file__), '../data')

csv = open(f"{dataDir}/2b_useful_data.csv", "r")

# 帧,时间,播放,评论,同时人数,同时人数不带加号,点赞,投币,收藏,转发
csv.readline()

datas : OrderedDict[datetime.datetime, str] = OrderedDict()

for line in csv.readlines():
    parts = line.split(',')
    time = datetime.datetime.fromisoformat(parts[1])
    datas[time] = line

datas = OrderedDict(sorted(datas.items(), key=lambda x: x[0]))

time0: Optional[datetime.datetime] = None

timePlays = []
timeLivePeople = []
timeCoins = []
timeLikes = []
timeFavorites = []
timeShares = []

lastPlays = 0
lastTime = None

# 原视频时长9分13秒
videoDuration = 553
for d, line in datas.items():
    parts = line.split(',')
    plays = float(parts[2])
    if time0 is None:
        # 跳过第一个点
        time0 = d
        lastTime = d
        lastPlays = plays
        continue
    # 从开始到现在这帧的时间
    deltatime = d - time0
    timestamp = d

    # 从上一帧到现在这帧的时间
    period = d - lastTime
    lastTime = d

    lastPlays = plays

    timePlays.append((timestamp, plays))

    if lastPlays == 0:
        lastPlays = plays
        continue

    # 同时观看人数
    livePeople = int(parts[5])
    timeLivePeople.append((timestamp,  livePeople))

    # 币，赞，收藏，转发
    coins = float(parts[7])
    timeCoins.append((timestamp, coins))
    likes = float(parts[6])
    timeLikes.append((timestamp, likes))
    favorites = float(parts[8])
    timeFavorites.append((timestamp, favorites))
    shares = float(parts[9])
    timeShares.append((timestamp, shares))



# 换个字体
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC']
matplotlib.rcParams['font.family'] = 'sans-serif'

# 时间-播放量
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

timePlays = np.array(timePlays)
ax1.plot(timePlays[:, 0], timePlays[:, 1], label='显示播放量')
ax1.set_xlabel('时间')
ax1.set_ylabel('播放量(万)')
ax1.legend()

timeLivePeople = np.array(timeLivePeople)
ax2.plot(timeLivePeople[:, 0], timeLivePeople[:, 1], label='同时观看人数', color='orange')
ax2.set_ylabel('同时观看人数')
ax2.legend()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M', tz=d.tzinfo))
ax1.xaxis.set_tick_params(rotation=90)
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.title('时间-播放量')
plt.subplots_adjust(bottom=0.25)
plt.savefig(f"{dataDir}/3a_time_plays.png")

# 时间-投币，赞，收藏，转发
plt.figure()
fig, ax = plt.subplots()
timeCoins = np.array(timeCoins)
ax.plot(timeCoins[:, 0], timeCoins[:, 1], label='投币')
timeLikes = np.array(timeLikes)
ax.plot(timeLikes[:, 0], timeLikes[:, 1], label='点赞')
timeFavorites = np.array(timeFavorites)
ax.plot(timeFavorites[:, 0], timeFavorites[:, 1], label='收藏')
timeShares = np.array(timeShares)
ax.plot(timeShares[:, 0], timeShares[:, 1], label='转发')
ax.set_xlabel('时间')
ax.set_ylabel('数量(万)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M', tz=d.tzinfo))
ax.xaxis.set_tick_params(rotation=90)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.title('时间-投币，赞，收藏，转发')
plt.legend()
plt.subplots_adjust(bottom=0.25)
plt.savefig(f"{dataDir}/3a_time_coins_likes_favorites_shares.png")
