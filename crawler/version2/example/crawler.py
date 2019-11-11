#!/usr/bin/python3
import re # for url extraction
import requests
import argparse
import json
import time
import random
import string
import os
from PIL import Image,ImageOps
from lxml import etree
from urllib import parse
from time import sleep # for request delay
from requests.exceptions import Timeout # for request timeout
from multiprocessing import cpu_count, Pool, TimeoutError # for parallel processing

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# number of processes for multiprocessing (using the number of CPUs in the system)
no_processes = cpu_count()


def randon_str(length = 8):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

def get_status(key):
    with open('status.json', 'r', encoding='utf-8') as f:
        data = f.read()
    status = json.loads(data)
    return status[key]

def save_status(data):
    with open('status.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))

def change_status(key, value):
    with open('status.json', 'r', encoding='utf-8') as f:
        data = f.read()
    status = json.loads(data)
    status[key] = value
    save_status(status)

def http_get(url):
    '''
    HTTP请求
    '''
    try:
        response = requests.get(url, timeout=(4, 5), verify=False)
    except Exception:
        print('The request time out or invalid url: ' + url)
        return []
    if response.status_code != 200:
        print("No result")
        return []
    return response.content

def match_url(content, xpath):
    '''
    获取图片链接
    '''
    html = etree.HTML(content)
    urls = html.xpath(xpath)
    return urls

def get_url(keyword, site):
    # 默认使用pixabay
    keyword = parse.quote(keyword)
    base_url   = "https://pixabay.com/images/search/"
    access_url = base_url + keyword
    xpath = '//*[@class="item"]/a/img/@src'
    if site == "pixabay":
        base_url   = "https://pixabay.com/images/search/"
        xpath = '//*[@class="item"]/a/img/@src'
        access_url = base_url + keyword
    elif site == "unsplash":
        base_url   = "https://unsplash.com/s/photos/"
        xpath = '//*[@class="_2zEKz"]/@src'
        access_url = base_url + keyword
    elif site == "pexels":
        base_url   = "https://www.pexels.com/search/"
        xpath = '//*[@class="photo-item__img"]/@src'
        access_url = base_url + keyword
    content = http_get(access_url)
    urls = match_url(content, xpath)
    return urls

def get_image_urls(keyword):
    urls = []
    sites = [
        "pixabay", 
        "unsplash", 
        "pexels"
    ]
    for site in sites:
        urls += get_url(keyword, site)
    urls = list(set(urls))
    return urls

# function to save image from url as file_name
def save_image(image_url):
    '''
    Save the image
    '''
    if "photo" not in image_url:
        return 0
    data = http_get(image_url)
    path = "image/" # Save the path
    file_name = randon_str(10) + ".png"
    if data is not None:
        with open(path + file_name, "wb") as f:
            f.write(data)
    # Shrink to 50px
    img = Image.open(path + file_name)
    img = ImageOps.fit(img, (50, 50), Image.ANTIALIAS)

    # Save the image
    os.remove(path + file_name)
    img.save(path + file_name)

def init():
    data = {
        "status": False,
        "start_time": int(time.time()),
        "end_time" : 0,
        "use_time" : 0,
        "count" : 0,
    }
    save_status(data)

def store_raw_images(keyword):
    '''
    Crawl the image
    '''
    init()
    image_urls = get_image_urls(keyword)
    multiple_responses = []

    with Pool(processes=no_processes) as pool:
        for image_url in image_urls:
            multiple_responses.append(pool.apply_async(save_image, (image_url,)))
        for res in multiple_responses:
            # print the status
            count = get_status("count")
            change_status("count", count + 1)
            start_time = get_status("start_time")
            end_time = int(time.time())
            use_time = end_time - start_time
            change_status("use_time", use_time)
            msg = f"count={count} use_time={use_time}"
            print(msg)
            try:
                res.get(timeout=5)
            except TimeoutError:
                print("Timeout: " + image_url)
    change_status("status", True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="cralwer keyword")
    args = parser.parse_args()
    if args.keyword:
        store_raw_images(args.keyword)