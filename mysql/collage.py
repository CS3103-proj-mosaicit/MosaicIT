import ImageDB
from PIL import Image
from PIL import ImageEnhance
import io
from image_crawler import store_raw_images
import base64


SCALE= 20


#src_img_path = './tea.jpg'
src_img_path = input("Please enter the path to the src img\n")


db = ImageDB.db()
db.init()

#print("The testing crawling may take 20s...")
#store_raw_images("sky")
print("Skipping crawl testing...")

im = Image.open(src_img_path).convert('LA')
#imm = im.thumbnail((15, 15))
px = im.load() #px is 2d matrix of pixel coordinates
#im.show()
width, height, = im.size
print('Size of width ' + str(width) + ' and height ' + str(height))

canvas_width = width*SCALE
canvas_height = height*SCALE
print('Using scale of 1:20 pixels...')
print('Creating new canvas with width ' 
        + str(canvas_width) + ' and height ' + str(canvas_height))

canvas = Image.new('RGB', (canvas_width, canvas_height), (0, 0, 255))
#canvas.show()
#print("file type " + str(type(im)))

num_tiles_needed = width * height

print("Opening "+ str(num_tiles_needed) + " testing images...")
tiles_selected = db.select_num(num_tiles_needed)

try:
    for i in range(0, width):
        canvas_x = i*SCALE
        for j in range(0, height):
            canvas_y = j*SCALE 
        
            print('px[' +str(i) +',' +str(j)+ ']'+ ' is ' + str(px[i,j]))
            px_l = px[i,j][0]
            px_a = px[i,j][1]
         
            print("Selecting pic close to " + str(px[i,j]))
        
            identifier = j%74
            if identifier == 0:
                identifier = 75

            print(str(identifier))
            db.cursor.execute("SELECT img FROM imagedb.image WHERE id=%s;", (identifier,))

            img = db.cursor.fetchone()
            img = db.raw_to_img(img[0])
        
            img.thumbnail((SCALE,SCALE))
            greyimg = img.convert('LA')
            #print(str(type(img))) #giving back nontype
        
    
            #brightness lvl here
        
            #factor = (260 - px_l)/200
            factor = px_l/255
            print(str(factor))
            enhancer_object = ImageEnhance.Brightness(greyimg)
            outimg = enhancer_object.enhance(factor) 

            #pasting here
            canvas.paste(outimg, (canvas_x, canvas_y))

except KeyboardInterrupt:
    print('\nStopping, saving partial image...')

finally:
    canvas.save("./mosaic.jpg")
    canvas.show()      
