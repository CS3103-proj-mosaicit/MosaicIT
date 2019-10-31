import mysql.connector
import zlib
import random
class ImageDB(object):
  def __init__(self):
    self.__connect()
    self.cursor.execute("CREATE DATABASE IF NOT EXISTS " + self.db_name)
    self.cursor.execute("USE " + self.db_name)
    self.cursor.execute("CREATE TABLE IF NOT EXISTS image(id INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY, rgb INT NOT NULL, hash INT UNIQUE NOT NULL, img MEDIUMBLOB)")
    

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


  def insert_img(self, img, rgb):
    h = zlib.crc32(img)
    try:
      self.cursor.execute("INSERT INTO imagedb.image(rgb, hash, img) VALUES (%s, %s, %s)", (rgb, h, img))
      self.conn.commit()
    except:
      return -1
    return 1

  def select_img(self, rgb):
    try:
      self.cursor.execute("SELECT * FROM imagedb.image WHERE rgb=%s", (rgb,))
      result = cursor.fetchone()[3]
      print(len(result))
    except:
      return -1
    return result

  def close_connection(self):
    self.cursor.close()
    self.conn.close()
