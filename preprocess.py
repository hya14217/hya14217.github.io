import os

from datetime import datetime
from PIL import Image
from pathlib import Path

dates = []

def process_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute}"

for img_file in Path("assets/upload").glob("*.jpg"):
    mtime = os.path.getmtime(img_file)
    dates.append(process_datetime(mtime))
    # 压缩
    o_size = os.path.getsize(img_file) / 1024
    thumbnail_outfile = os.path.join(img_file.parent.parent, "thumbnail", img_file.name)
    img_outfile = os.path.join(img_file.parent.parent, "img", img_file.name)
    if o_size <= 150:
        im = Image.open(img_file)
        im.save(thumbnail_outfile, quality=80)
        im.save(img_outfile, quality=80)
        continue
    quality = 80
    while o_size > 150:
        im = Image.open(img_file)
        im.resize((1920, im.size[1]*1920//im.size[0])).save(img_outfile, quality=quality)
        im.resize((640, im.size[1]*640//im.size[0])).save(thumbnail_outfile, quality=quality)
        if quality - 10 < 0:
            break
        quality -= 10
        o_size = os.path.getsize(thumbnail_outfile) / 1024

with open("dates.js", "w", encoding="utf-8") as fout:
    fout.write(f"var dates = {str(dates)}")
