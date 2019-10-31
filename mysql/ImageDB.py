import io
import mysql.connector
import numpy as np
import random
import zlib
from PIL import Image
class db(object):
  def __init__(self):
    self.__connect()
    self.cursor.execute("CREATE DATABASE IF NOT EXISTS " + self.db_name)
    self.cursor.execute("USE " + self.db_name)
    self.cursor.execute("CREATE TABLE IF NOT EXISTS image(id INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY, rgb INT NOT NULL, hash INT NOT NULL, img MEDIUMBLOB)")
    

  def __connect(self):
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
    pic = Image.open(io.BytesIO(img))
    im = np.array(pic)
    # get shape
    w,h,d = im.shape
    # change shape
    im.shape = (w*h, d)
    # get average
    rgb = tuple(int(round(x)) for x in tuple(im.mean(axis=0)))
    print(rgb)
    return int('%02x%02x%02x' % rgb, 16)

  def insert_img(self, img):
    h = zlib.crc32(img)
    rgb = self.avg_rgb(img)
    try:
      self.cursor.execute("INSERT INTO imagedb.image(rgb, hash, img) VALUES (%s, %s, %s)", (rgb, h, img))
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

  def close_connection(self):
    self.cursor.close()
    self.conn.close()
