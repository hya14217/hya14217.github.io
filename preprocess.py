import os

from PIL import Image
from pathlib import Path


infos = []

for img_file in Path("upload").glob("*.jpg"):
    # 压缩
    o_size = os.path.getsize(img_file) / 1024
    if o_size <= 500:
        continue
    outfile = os.path.join(img_file.parent.parent, "assets/img", img_file.name)
    quality = 80
    while o_size > 500:
        im = Image.open(img_file)
        im.save(outfile, quality=80)
        if quality - 10 < 0:
            break
        quality -= 10
        o_size = os.path.getsize(outfile) / 1024
