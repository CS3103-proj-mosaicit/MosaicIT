import mysql.connector
import binascii
db_name = "imagedb"
conn = mysql.connector.connect(host='localhost',
                              user='root',
                              port=3306,
                              password='3103',
                              use_pure=True)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS " + db_name)
cursor.execute("USE " + db_name)
cursor.execute("CREATE TABLE IF NOT EXISTS image(id INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY, rgb INT NOT NULL, hash INT UNIQUE NOT NULL, img MEDIUMBLOB)")
f=open('/Users/zhangjingchen/Desktop/img.jpg', 'rb')
data=f.read()
h=binascii.crc32(data)
# cursor.execute("INSERT INTO imagedb.image(rgb, hash, img) VALUES (%s, %s, %s)", (0x010305, h, data))
# conn.commit()
cursor.execute("SELECT img FROM imagedb.image WHERE id=1")
result = cursor.fetchone()[0]
print(len(result))
f=open("/Users/zhangjingchen/Desktop/img2.jpg", 'wb')
f.write(result)
f.close()

# cursor = mysql.connector.connect(host='localhost',
#                               user='root',
#                               password='3103')
                    
cursor.close()
conn.close()
