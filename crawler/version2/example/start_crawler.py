#!/usr/bin/env python3
import os

def read_keyword():
    with open("keyword.txt", "r") as f:
        ret = f.readlines()
    return ret

def start():
    for keyword in read_keyword():
        print(f"start Keyword={keyword}")
        cmd = f"python3 crawler.py --keyword {keyword}"
        os.system(cmd)


if __name__ == "__main__":
    start()
