import json
import os, sys
from concurrent.futures import ProcessPoolExecutor
from typing import Optional

from paddleocr import PaddleOCR

dataDir = os.path.join(os.path.dirname(__file__), "../data")

ocr = PaddleOCR(use_angle_cls=False, lang="ch")

f = open(f"{dataDir}/2a_ocr.jsonl", "w+")

executor = ProcessPoolExecutor(max_workers=10)
tasks = []
futures = {}

for file in os.listdir(f"{dataDir}/top_banner"):
    frameIndex = file.split(".")[0]
    tasks.append(frameIndex)


def process(dir, frameIndex) -> Optional[str]:
    filePath = f"{dataDir}/{dir}/{frameIndex}.png"
    result = ocr.ocr(filePath, det=True, cls=False)
    if len(result) != 1:
        print("ocr failed:", filePath)
        return None
    line = result[0]
    texts = []
    for area in line:
        texts.append(area[1][0])
    return texts

dirs = ("top_banner", "bottom_banner", "live_people", "time", "date")

for frameIndex in tasks:
    for dir in dirs:
        future = executor.submit(process, dir, frameIndex)
        futures[frameIndex] = futures.get(frameIndex, {})
        futures[frameIndex][dir] = future

for frameIndex, futureDict in futures.items():
    results = {"index": frameIndex}
    for dir in dirs:
        future = futureDict.get(dir)
        if not future:
            print("future not found for ", frameIndex, dir)
            continue
        result = future.result()
        if not result:
            continue
        results[dir] = result
    f.write(json.dumps(results, ensure_ascii=False) + "\n")
    f.flush()

f.close()
