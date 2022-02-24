import os

from datetime import datetime
from PIL import Image
from pathlib import Path

dates = []

def process_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute}"

for img_file in Path("assets/upload").glob("*.jpg"):
    # 压缩
    o_size = os.path.getsize(img_file) / 1024
    if o_size <= 500:
        continue
    outfile = os.path.join(img_file.parent.parent, "img", img_file.name)
    quality = 80
    while o_size > 500:
        im = Image.open(img_file)
        im.save(outfile, quality=80)
        if quality - 10 < 0:
            break
        quality -= 10
        o_size = os.path.getsize(outfile) / 1024
    mtime = os.path.getmtime(img_file)
    dates.append(process_datetime(mtime))

with open("dates.js", "w", encoding="utf-8") as fout:
    fout.write(f"var dates = {str(dates)}")
