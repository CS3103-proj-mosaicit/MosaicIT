import io
import mysql.connector
import numpy as np
import random
import zlib
from PIL import Image

class db(object):
    def init(self):
        self.connect()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS " + self.db_name)
        self.cursor.execute("USE " + self.db_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS image(id INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY, r INT NOT NULL, g INT NOT NULL, b INT NOT NULL, hash INT NOT NULL UNIQUE, img MEDIUMBLOB)")

    def connect(self):
        self.db_name = "imagedb"
        self.conn = mysql.connector.connect(host='localhost',
                user='root',
                port=3306,
                password='3103',
                use_pure=True)
        self.cursor = self.conn.cursor()

    def test(self):
        # this function test: insert, select
        self.testing_path='./'
        f = open(self.testing_path + 'img.jpg', 'rb')
        data = f.read()
        h = zlib.crc32(data)
        try:
            self.cursor.execute("INSERT INTO imagedb.image(r, g, b, hash, img) VALUES (%s, %s, %s, %s, %s)", (0, 0, 0, h, data))
            self.conn.commit()
        except:
            pass
        self.cursor.execute("SELECT img FROM imagedb.image WHERE rgb=%s", (0x010305,))
        result = self.cursor.fetchone()[0]
        print(len(result))
        f=open(self.testing_path + 'img2.jpg', 'wb')
        f.write(result)
        f.close()

    def avg_rgb(self, img):
        pic = self.raw_to_img(img)
        im = np.array(pic)
        # get shape
        w,h,d = im.shape
        # change shape
        im.shape = (w*h, d)
        # get average
        rgb = tuple(int(round(x)) for x in tuple(im.mean(axis=0)))
        return int('%02x%02x%02x' % rgb, 16)


    def insert_img(self, raw_img):
        try:
            img = self.resize_cut(self.raw_to_img(raw_img))
            raw_img = self.img_to_raw(img)
            h = zlib.crc32(raw_img)
            rgb = self.avg_rgb(raw_img)
            r, g, b = rgb // 65536, (rgb - rgb // 65536 * 65536) // 256, rgb % 256
            self.cursor.execute("INSERT INTO imagedb.image(r, g, b, hash, img) VALUES (%s, %s, %s, %s, %s)", (r, g, b, h, raw_img))
            self.conn.commit()
            print((r, g, b))
        except:
            return -1
        return 1

    def select_rgb(self, rgb):
        try:
            r, g, b = rgb // 65536, (rgb - rgb // 65536 * 65536) // 256, rgb % 256
            self.cursor.execute("SELECT img FROM imagedb.image WHERE r=%s AND g=%s And b=%s", (r, g, b))
            result = self.cursor.fetchone()[0]
            # print(len(result))
        except:
            return -1
        return result

    def select_rough_rgb(self, rgb):
        img = None
        step = 10
        r, g, b = rgb // 65536, (rgb - rgb // 65536 * 65536) // 256, rgb % 256
        while not img:
            try:
                self.cursor.execute("SELECT img FROM imagedb.image WHERE r > %s AND r < %s AND g > %s AND g < %s AND b > %s And b < %s;", (r - step, r + step, g - step, g + step, b - step, b + step))
                step += 10
                img = self.cursor.fetchone()[0]
            except:
                continue
        return img

    def select_num(self, num):
        self.cursor.execute("SELECT * FROM imagedb.image LIMIT " + str(num))
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def resize_cut(self, img): # @raw bytes img, any size =. 300 * 300 pix
        size=img.size
        if(size[0] > size[1]):
            img = img.resize((int(size[0]/size[1]*300), 300))
            size = img.size
            img = img.crop(( int((size[0] - 300) / 2), 0, int((size[0] + 300) / 2), 300))
        else:
            img = img.resize((300, int(size[1]/size[0]*300)))
            size = img.size
            img = img.crop(( 0, int( (size[1] - 300) / 2), 300, int( (size[1] + 300) / 2) ))
        return img

    def raw_to_img(self, raw_img): # @img obj
        return Image.open(io.BytesIO(raw_img))

    def img_to_raw(self, img):
        byteIO = io.BytesIO()
        img.save(byteIO, format='PNG')
        return byteIO.getvalue()

    def rgb_to_hex(self, r, g, b):
        return int((r<<16) + (g<<8) + b)

    #takes in rgb tuple
    def select_closest_rgb(self, rgb):
        r, g, b = rgb
        sampled_src = np.array([r,g,b])

        candidate = {'image_data':'', 'distance': ((255**2)*3)**0.5}

        try:
            self.cursor.execute("SELECT id FROM imagedb.image;")
            #identifiers = self.cursor.fetchall()
            identifiers= [x[0] for x in self.cursor.fetchall()] 
            #print('IDENTIFIERS: ' +str(identifiers))
            #print(str(type(identifiers)))

            for identifier in identifiers:
                print('inside my select closest rgb: ' +str(identifier) + '\n')
                self.cursor.execute("SELECT r,g,b,img  FROM imagedb.image WHERE id=%s;", (identifier,) )
                #print('a')
                test_r, test_g, test_b, test_imagedata = self.cursor.fetchone()
                print('test_r ' + str(test_r) + 'test_g ' + str(test_g) + 'test_b ' + str(test_b))
                test_point = np.array([test_r, test_g, test_b]) 
                print('calculating distance diff')
                test_dist = ((test_r - r)**2 + (test_g - g)**2 + (test_b - b)**2)**0.5
                print('test_dist is ' +str(test_dist))

                if test_dist < candidate['distance']:
                    print(str(test_dist) + ' < ' + str(candidate['distance']))
                    candidate['image_data'] = test_imagedata
                    candidate['distance'] = test_dist
                else:
                    print('last distance' + str(candidate['distance'] +' was closer'))
        except:
            pass

        return candidate['image_data']

