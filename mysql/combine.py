import ImageDB
import numpy as np
import sys
from PIL import Image

PIX_SIZE = 20
SIZE = 30
#H = 30




w = 0
h = 0
def resize_img(img):
  global w, h
  size=img.size
  if(size[0] < size[1]):
    w = int(size[0]/size[1]*SIZE)
    h = SIZE
    img = img.resize((w, h))
  else:
    w = SIZE
    h = int(size[1]/size[0]*SIZE)
    img = img.resize((w, h))
  return img

def main():
  global w, h
  try:
    db = ImageDB.db()
    db.init()
  except:
    print("Failed to connect db...")
    return
  path = sys.argv[1]
  # with open(path, 'rb') as f:
  #   data=f.read()
  # db=ImageDB.db()
  # input_img = db.raw_to_img(data)
  # input_img = resize_img(input_img)
  # input_img.show()
  im = resize_img(Image.open(path))
  pix = im.load()
  im.show()
  print((w, h))
  print(pix[0,0])
  r, g, b = pix[0, 0]
  # db.raw_to_img(db.select_rough_rgb(r*65536 + g*256 + b)).show()
  final = Image.new('RGB', (w*PIX_SIZE, h*PIX_SIZE), (255,255,255))
  for y in range(0, w):
    for x in range(0, h):
      print(pix[y, x])
      rgb = db.rgb_to_int(pix[y, x])
      pix_img = db.raw_to_img(db.select_rough_rgb(rgb)).resize((PIX_SIZE, PIX_SIZE))
      final.paste(pix_img, (y*PIX_SIZE, x*PIX_SIZE))
      print(pix[y, x])
  final.show()
  file_name = path.split('/')[-1]
  final.save(path.replace(file_name, '') + 'mosaic ' + file_name)
  print("File saved to original path.")

if __name__ == '__main__':
  main()
