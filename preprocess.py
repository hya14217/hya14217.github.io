import os
import json

from datetime import datetime
from PIL import Image
from pathlib import Path


ZIP_THRESHOLD = 150
ZIP_RATIO = 80
QUALITY_STEP =10
THUMBNAIL_SIZE = 480
PREVIEW_SIZE = 1920


def process_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return f"{dt.year}/{dt.month}/{dt.day} {dt.hour:2}:{dt.minute:2}:{dt.minute:2}"


def preprocess(img_file):
    # 压缩
    quality = ZIP_RATIO
    o_size = os.path.getsize(img_file) / 1024
    thumbnail_outfile = os.path.join(img_file.parent.parent, "thumbnail", img_file.name)
    img_outfile = os.path.join(img_file.parent.parent, "img", img_file.name)
    if o_size <= ZIP_THRESHOLD:
        im = Image.open(img_file)
        im.save(thumbnail_outfile)
        im.save(img_outfile)
        return
    while o_size > ZIP_THRESHOLD:
        im = Image.open(img_file)
        im.resize((PREVIEW_SIZE, im.size[1]*PREVIEW_SIZE//im.size[0])).save(img_outfile, quality=quality)
        im.resize((THUMBNAIL_SIZE, im.size[1]*THUMBNAIL_SIZE//im.size[0])).save(thumbnail_outfile, quality=quality)
        if quality - QUALITY_STEP < 0:
            return
        quality -= QUALITY_STEP
        o_size = os.path.getsize(thumbnail_outfile) / 1024


def main():
    for img_file in Path("assets/upload").glob("*.jpg"):
        preprocess(img_file)


if __name__ == "__main__":
    main()
