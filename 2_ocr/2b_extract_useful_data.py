import re
import os,sys
import json
import datetime

dataDir = os.path.join(os.path.dirname(__file__), '../data')

f = open(f"{dataDir}/2a_ocr.jsonl", "r")
fw = open(f"{dataDir}/2b_useful_data.csv", "w")

wanRe = re.compile(r'③*(?P<num>\d+(\.\d+)*)万')
livePeopleRe = re.compile(r'^(?P<num>\d+\+*)人正在看')

# bom
fw.write("\ufeff")
fw.write("帧,时间,播放,评论,同时人数,同时人数不带加号,点赞,投币,收藏,转发\n")

for line in f.readlines():
    data = json.loads(line)
    index = data['index']

    # 时间
    time = data['time'][0]
    # 日期
    date = data['date'][0]

    try:
        dt = datetime.datetime.strptime(f"{date} {time}+0800", "%Y/%m/%d %H:%M:%S%z")
    except ValueError:
        print(f"{index}: time not match: {date} {time}")
        continue
    isoDate = dt.isoformat()

    # 播放量
    plays = data['top_banner'][0]
    # 评论
    comments = data['top_banner'][1]

    if plays == "全站排行榜最高第1名>":
        plays = data['top_banner'][1]
        comments = data['top_banner'][2]
    # 简单校验
    if not (m := wanRe.match(plays)):
        print(f"{index}: plays not match: {plays}")
        continue
    plays = m.group('num')
    if not (m := wanRe.match(comments)):
        print(f"{index}: comments not match: {comments}")
        continue
    comments = m.group('num')

    livePeople = data['live_people'][0]
    if not (m := livePeopleRe.match(livePeople)):
        print(f"{index}: live people not match: {livePeople}")
        continue
    livePeople = m.group('num')
    livePeopleNoPlus = livePeople.replace('+', '')

    # 点赞
    likes = data['bottom_banner'][0]
    if not (m := wanRe.match(likes)):
        print(f"{index}: likes not match: {likes}")
        continue
    likes = m.group('num')

    # 投币
    coins = data['bottom_banner'][1]
    if not (m := wanRe.match(coins)):
        print(f"{index}: coins not match: {coins}")
        continue
    coins = m.group('num')

    # 收藏
    favorites = data['bottom_banner'][2]
    if not (m := wanRe.match(favorites)):
        print(f"{index}: favorites not match: {favorites}")
        continue
    favorites = m.group('num')

    # 转发
    shares = data['bottom_banner'][3]
    if not (m := wanRe.match(shares)):
        print(f"{index}: shares not match: {shares}")
        continue
    shares = m.group('num')

    # 写csv
    fw.write(f"{index},{isoDate},{plays},{comments},{livePeople},{livePeopleNoPlus},{likes},{coins},{favorites},{shares}\n")
    fw.flush()
