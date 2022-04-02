import os
import json

from pathlib import Path
from preprocess import process_datetime

def parse_articles():
    result = []
    for article_file in Path("articles").glob("*.md"):
        content = open(article_file, "r", encoding="utf-8").read()
        mtime = process_datetime(os.path.getmtime(article_file))
        result.append({"content": content, "mtime": mtime})
    code = json.dumps(result, ensure_ascii=False)
    code = f"var articles = {code};"
    with open("article.js", "w", encoding="utf-8") as fout:
        fout.write(code)


if __name__ == "__main__":
    parse_articles()
