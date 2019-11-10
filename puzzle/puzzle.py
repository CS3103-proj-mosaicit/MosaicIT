import os
import argparse
import time
import random
import math
import sys
import json
from PIL import Image,ImageOps
from multiprocessing import Pool
from colorsys import rgb_to_hsv

SLICE_SIZE = 30
OUT_SIZE = 1000
IN_DIR = "../crawler/image/"
OUT_DIR = "output/"
DIFF_FAR = 100
REPATE = 1

def get_avg_color(img):
    width, height = img.size
    pixels = img.load()
    if type(pixels) is not int:
        data = []
        for x in range(width):
            for y in range(height):
                cpixel = pixels[x, y]
                data.append(cpixel)
        h = 0
        s = 0
        v = 0
        count = 0
        for x in range(len(data)):
            r = data[x][0]
            g = data[x][1]
            b = data[x][2]
            count += 1
            hsv = rgb_to_hsv(r / 255.0,g / 255.0,b / 255.0)
            h += hsv[0]
            s += hsv[1]
            v += hsv[2]

        hAvg = round(h / count,3)
        sAvg = round(s / count,3)
        vAvg = round(v / count,3)

        if count > 0:

            return (hAvg,sAvg,vAvg)
        else:
            raise IOError("Failed to read image status")
    else:
        raise IOError("PIL - failed to read image status")


def find_closiest(color, list_colors):
    cur_closer = False
    arr_len = 0
    FAR = DIFF_FAR
    for cur_color in list_colors:
        n_diff = math.sqrt(math.pow(math.fabs(color[0]-cur_color[0]), 2) + math.pow(math.fabs(color[1]-cur_color[1]), 2) + math.pow(math.fabs(color[2]-cur_color[2]), 2))
        if n_diff < FAR and cur_color[3] <= REPATE:
            FAR = n_diff
            cur_closer = cur_color
    if not cur_closer:
        raise ValueError("Don't have enough similar images，recommend to set similar images.")
        clean_cache()
    cur_closer[3] += 1
    return "({}, {}, {})".format(cur_closer[0],cur_closer[1],cur_closer[2])


def make_puzzle(img, color_list):
    width, height = img.size
    background = Image.new('RGB', img.size, (255,255,255))
    total_images = math.floor((width * height) / (SLICE_SIZE * SLICE_SIZE))
    now_images = 0
    for y1 in range(0, height, SLICE_SIZE):
        for x1 in range(0, width, SLICE_SIZE):
            try:
                y2 = y1 + SLICE_SIZE
                x2 = x1 + SLICE_SIZE
                new_img = img.crop((x1, y1, x2, y2))
                color = get_avg_color(new_img)
                close_img_name = find_closiest(color, color_list)
                close_img_name = OUT_DIR + str(close_img_name) + '.jpg'
                paste_img = Image.open(close_img_name)
                now_images += 1
                now_done = math.floor((now_images / total_images) * 100)
                if now_done >= 100:
                    now_done = 100
                change_status("progress", now_done)
                r = '\r[{}{}]{}%'.format("#"*now_done," " * (100 - now_done),now_done)
                sys.stdout.write(r)                          
                sys.stdout.flush()    
                background.paste(paste_img, (x1, y1))
            except IOError:
                print('Failed to make puzzle!')
    return background


def get_image_paths():
    paths = []
    suffixs = ['png','jpg'];
    for file_ in os.listdir(IN_DIR):
        suffix = file_.split('.',1)[1]
        if suffix in suffixs:
            paths.append(IN_DIR + file_)
        else:
            print("Not an image:%s" % file_)
    if len(paths) > 0:
        print("In total we find %s" % len(paths) + " images.")
    else:
        raise IOError("Failed to find any graph!")

    return paths 

def resize_pic(in_name,size):
    img = Image.open(in_name)
    return img

def resize_input_pic(in_name):
    img = Image.open(in_name)
    width, height = img.size
    # Set the size of the image to be within 1000px
    if width > height:
        width  = 800
        height = int(800 / width * height)
    else:
        width  = int(800 / width * width)
        height = 800
    

    print("resize Pic Width = {}, Height = {}".format(width,height))
    img = ImageOps.fit(img, (width, height), Image.ANTIALIAS)
    os.remove(in_name)
    img.save(in_name)

def convert_image(path):
    try:
        img = resize_pic(path,SLICE_SIZE)
        color = get_avg_color(img)
        img.save(str(OUT_DIR) + str(color) + ".jpg")
    except:
        return False


def convert_all_images():
    paths = get_image_paths()
    print("Creating mosaics...")
    pool = Pool()
    pool.map(convert_image, paths)
    pool.close()
    pool.join()   

def read_img_db():
    img_db = []
    for file_ in os.listdir(OUT_DIR):
        if file_ == 'None.jpg':
            pass
        else:     
            file_ = file_.split('.jpg')[0]
            file_ = file_[1:-1].split(',')
            file_ = list(map(float,file_))
            file_.append(0)
            # print(file_)
            img_db.append(file_)    
    return img_db

def clean_cache():
    path_data = "puzzle/output/"
    for i in os.listdir(path_data):
        file_data = path_data + i
        if os.path.isfile(file_data) == True:
            os.remove(file_data)

def get_status(key):
    with open('puzzle/status.json', 'r', encoding='utf-8') as f:
        data = f.read()
    status = json.loads(data)
    return status[key]

def change_status(key, value):
    with open('puzzle/status.json', 'r', encoding='utf-8') as f:
        data = f.read()
    status = json.loads(data)
    status[key] = value
    with open('puzzle/status.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(status))

def init():
    data = {
        "status": False,
        "start_time": int(time.time()),
        "output": "",
        "end_time" : 0,
        "use_time" : 0,
        "progress" : 0
    }
    with open('puzzle/status.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))

if __name__ == '__main__':
    init()
    parse = argparse.ArgumentParser()
    parse.add_argument("-i",'--input',required=True,help='input image')
    parse.add_argument("-d", "--db", type=str, required=True,help="source database")
    parse.add_argument("-t", "--temp", type=str, required=True,help="out directory")
    parse.add_argument("-o", "--output", type=str, required=True,help="out directory")
    parse.add_argument("-s","--save",type=str,required=False,help="create image but not create database")
    parse.add_argument("-is",'--inputSize',type=int, required=False,help="inputSize")
    parse.add_argument("-os",'--outputSize',type=int, required=False,help="outputSize")
    parse.add_argument("-r",'--repate',type=int, required=False,help="repate number")
    parse.add_argument("-far",'--far',type=int, required=False,help="image difference")
    args = parse.parse_args()
    start_time = time.time()
    args = parse.parse_args()
    image = args.input
    
    if args.db:
        IN_DIR = args.db
    if args.temp:
        OUT_DIR = args.temp
    if args.output:
        OUTPUT_FILENAME = args.output
    if args.inputSize:
        SLICE_SIZE = args.inputSize
    if args.outputSize:
        OUT_SIZE = int(args.outputSize)
    if not args.save:
        convert_all_images()
    if args.repate:
        REPATE = args.repate
    if args.far:
        DIFF_FAR = args.far

    change_status("start_time", int(time.time()))

    resize_input_pic(image)
    img = resize_pic(image,OUT_SIZE)
    list_of_imgs = read_img_db()
    out = make_puzzle(img, list_of_imgs)
    img = Image.blend(out, img, 0.5)
    img.save(OUTPUT_FILENAME)
    change_status("output", OUTPUT_FILENAME)

    # Clean up
    clean_cache()
    end_time = int(time.time())
    use_time = int(end_time - start_time)
    change_status("end_time", end_time)
    change_status("use_time", use_time)
    change_status("status", True)
