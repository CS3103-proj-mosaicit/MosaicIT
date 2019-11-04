# To cralw image with keywords
1. Modify keywords.txt
```
some
keywords
write
to
this
file
```
2. Run
```
python3 cralw.py
```

## This is to keep track of keywords cralwed
```
flower
sky
snow
sea
```
Note: cralwed images stored in `db.sql`

# Setup Flow
## Docker -> Python module -> Testing script


## For Docker start:
execute
```
docker-compose -f stack.yml up
```

## MySQLWorkench
You may want this application to help access MySQL.

## MySQL Setup Guide
### Docker
We adopt docker as a tool to run MySQL image for security reason.(no external access to our database) 
`Download Docker from `
* [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac) - The Docker image for Mac
* [Docker](https://hub.docker.com/?overlay=onboarding) - The Docker image for Windows

`Note that it may be required to create your own Docker account.`

After running Docker, execute
```
sh ./execute_this.sh 
```
Then MySQL will be available at port 3306 (You may change accordingly in the stack.yml file)

`ROOT account password:`
```
3103
```
## Python module

```
import ImageDB
db = ImageDB.db()

# where img is binary jpg/png file; return size of img in bytes
db.insert_img(img) 


# input wanted rgb decimal number; return a img in bytes
db.select_img(rgb)

# input a img in bytes; return the average rgb in decimal
db.avg_rgb(img) 
```

## Testing

```
python3 testing_script.py
```

# ImageDB Available functions

**Functions related to database**

|Functions|Parameter|Return|
----------|------------|------|
|init|None|None; Initialize connection|
|avg_rgb|img_in_bytes|a tuple of rgb e.g (114, 99, 150)|
|insert_img|img_in_bytes| 1 if succeed / -1 if failed |
|select_rgb|int_rgb|img_in_bytes / -1 if failed|
|select_rough_rgb|int_rgb|img_in_bytes / None if empty db|
|select_ten|None|an array of ten imgs in bytes|
|close_connection|None|None; Close db connection|



**Functions to modify Image**

|Functions|Parameter|Return|
----------|------------|------|
|resize_cut|img_obj|img_obj with size 300*300|
|raw_to_img|img_in_bytes|img_obj|
|img_to_raw|img_obj|img_in_bytes|

