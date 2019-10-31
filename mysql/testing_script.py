import ImageDB
from PIL import Image
import io
db = ImageDB.db()
db.tesging_path='./'# rmb to put an image img.jpg under 

# Testing databse insert/select
db.test()


# Testing rgb calculation
f=open('img.jpg','rb')
data=f.read()
f.close()
avg = db.avg_rgb(data)
print(avg)

# Testing image insertion
print("Inserting image!")
print(db.insert_img(data))

# Testing image retrive
img = db.select_img(avg)
if img != -1:
  Image.open(io.BytesIO(img)).show()
else:
  print("Error in selecting image!")