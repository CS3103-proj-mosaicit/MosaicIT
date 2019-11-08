# Smart Photomosaic

## Frontend & Backend:
- [python flask](http://flask.palletsprojects.com/en/1.1.x/)
- [html5](https://en.wikipedia.org/wiki/HTML5)
- [css3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)


Homepage:

![alt text](https://github.com/CS3103-proj-mosaicit/frontend/blob/master/images/readme-home.png)

Upload Page:
![alt text](https://github.com/CS3103-proj-mosaicit/frontend/blob/master/images/readme-upload.png)

Gallery Page:
![alt text](https://github.com/CS3103-proj-mosaicit/frontend/blob/master/images/readme-gallery1.png)

![alt text](https://github.com/CS3103-proj-mosaicit/frontend/blob/master/images/readme-gallery2.png)

## Crawling algorithm:
### Websites used for image collection:

- [pixabay](https://pixabay.com/)
- [unsplash](https://unsplash.com/)
- [pexels](https://www.pexels.com/)

### Available Functions:
**Functions to retrieve Query URL based on a provided keyword**

|Functions|Parameter|Return|
----------|------------|------|
|to_pixabay_url|keyword|Query URL for *pixabay*|
|to_unsplash_url|keyword|Query URL for *unsplash*|
|to_pexels_url|keyword|Query URL fpr *pexels*|

**Functions to retrieve image URLs**

|Functions|Paramete|Return|
----------|------------|------|
|scrape_pixabay|keyword|list of image URLs from *pixabay*|
|scrape_unsplash|keyword|list of image URLs from *unsplash*|
|scrape_pexels|keyword|list of image URLs from *pexels*|
|get_image_urls|keyword|list of image URLs from all the stated websites|

**Functions to process image URL**

|Functions|Parameter(s)|Return|
----------|------------|------|
|raw_image|image_url|raw image data (`None` if fail)|
|save_image|file_name, image_url|`None` (save image as `file_name`)|

**Functions to crawl and store images based on a keyword**

|Functions|Parameter|Return|
----------|------------|------|
|store_raw_images|keyword|`None` (store images data crawl based on a keyword into the database)|

*Note: store_raw_images make use of multiprocessinng with 0.05s sleep*

## Picture Storage:
## To crawl image with keywords
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
python3 crawl.py
```

### This is to keep track of keywords crawled
```
flower
sky
snow
sea
sunset
star
cat
dog
```
Count: 226
Note: crawled images stored in `db.sql`

### Setup Flow
### Docker -> Python module -> Testing script


### For Docker start:
1. Execute
```
docker-compose -f stack.yml up
```
2. Then `command + t` to open a new terminal
3. Insert existing image data by executing
```
docker ps # to get the container ID
cp ./db.sql CONTAINER_ID:/db.sql
docker exec -it CONTAINER_ID bash
$bash mysql -u root -p < /db.sql # root password mentioned below
`control + d` to exit
```
4. Testing
run `python3 testing_script.py` to test extracting image from database.

### MySQLWorkench
You may want this application to help access MySQL.

### MySQL Setup Guide
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
### Testing

```
python3 testing_script.py
```

## ImageDB Available functions

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



## Picture combination:

### Repo used for Mosaic Tool

[https://github.com/NoisyWinds/puzzle.git](https://translate.google.com/translate?hl=en&sl=zh-CN&tl=en&u=https://github.com/NoisyWinds/puzzle)


### Modules to be Optimised/Replaced

 - Scraper
 - Storage
 + UI will be added on

### Usage
python3 puzzle.py -i $<$path to original img> -d $<$path to where imgs are stored> -o $<$path to output> 


**will be modified later when the imgs from the db are integrated into the tool**


## Contributors
- [Ahn TaeGyu](https://github.com/Letm3through)

- [Fan Yuting](https://github.com/April0616)

- [Zhang Jingchen](https://github.com/jingchen-z)

- [Lucy Chan](https://github.com/lucydotc)
