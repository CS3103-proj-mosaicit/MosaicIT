import ImageDB
from PIL import Image
import io
from image_crawler import store_raw_images
import base64


SCALE= 20


#src_img_path = './tea.jpg'
src_img_path = input("Please enter the path to the src img")


db = ImageDB.db()
db.init()

#print("The testing crawling may take 20s...")
#store_raw_images("sky")
print("Skipping crawl testing...")

im = Image.open(src_img_path)
imm = im.thumbnail((15, 15))
px = im.load() #px is 2d matrix of pixel coordinates
#im.show()
width, height, = im.size
print('Resizing width to ' + str(width) + ' and height to ' + str(height))

canvas_width = width*SCALE
canvas_height = height*SCALE
print('Using scale of 1:20 pixels...')
print('Creating new canvas with width ' 
        + str(canvas_width) + ' and height ' + str(canvas_height))

canvas = Image.new('RGB', (canvas_width, canvas_height), (0, 0, 255))
#canvas.show()
print("file type " + str(type(im)))

num_tiles_needed = width * height

print("Opening "+ str(num_tiles_needed) + " testing images...")
#tiles_selected = db.select_num(num_tiles_needed)
tiles_selected = db.select_num(30)

for i in range(0, width):
    canvas_x = i*SCALE
    for j in range(0, width):
        canvas_y = j*SCALE 
        
        print('px[' +str(i) +',' +str(j)+ ']'+ ' is ' + str(px[i,j]))
        px_r = px[i,j][0]
        px_g = px[i,j][1]
        px_b = px[i,j][2]
        hexcolour = db.rgb_to_hex(px_r,px_g,px_b)
        #print(type(hexcolour))
         
        print("Selecting pic close to " + str(px[i,j]))
        #img = db.select_rough_rgb(hexcolour)
        img = db.select_closest_rgb((px[i,j]))   
        #print(base64.b64encode(img))
       
        #rgb=db.avg_rgb(img)
        #r, g, b = rgb // 65536, (rgb - rgb // 65536 * 65536) // 256, rgb % 256
        #print("Input rgb: " +str((px_r, px_g, px_b)) +", output rgb:" + str((r, g, b)))
        #db.raw_to_img(img).show() 
        img = db.raw_to_img(img)
        #print(str(type(img))) #giving back nontype
        img.thumbnail((SCALE,SCALE))
        #print(str(type(img))) #giving back nontype

        
        #pasting here
        canvas.paste(img, (canvas_x, canvas_y))
        canvas.save("./mosaic.jpg")


canvas.show()      
