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
    self.cursor.execute("CREATE TABLE IF NOT EXISTS image(id INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY, rgb INT NOT NULL, hash INT NOT NULL UNIQUE, img MEDIUMBLOB)")
    

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
      self.cursor.execute("INSERT INTO imagedb.image(rgb, hash, img) VALUES (%s, %s, %s)", (0x010305, h, data))
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
    print(rgb)
    return int('%02x%02x%02x' % rgb, 16)

  def insert_img(self, raw_img):
    img = self.resize_cut(self.raw_to_img(raw_img))
    raw_img = self.img_to_raw(img)
    h = zlib.crc32(raw_img)
    rgb = self.avg_rgb(raw_img)
    try:
      self.cursor.execute("INSERT INTO imagedb.image(rgb, hash, img) VALUES (%s, %s, %s)", (rgb, h, raw_img))
      self.conn.commit()
    except:
      return -1
    return 1

  def select_img(self, rgb):
    try:
      self.cursor.execute("SELECT img FROM imagedb.image WHERE rgb=%s", (rgb,))
      result = self.cursor.fetchone()[0]
      # print(len(result))
    except:
      return -1
    return result

  def select_ten(self):
    self.cursor.execute("SELECT * FROM imagedb.image LIMIT 10")
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

