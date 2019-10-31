# Smart Photomosaic

## Frontend & Backend:

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

## Picture combination:

### Repo used for Mosaic Tool

[https://github.com/NoisyWinds/puzzle.git](https://translate.google.com/translate?hl=en&sl=zh-CN&tl=en&u=https://github.com/NoisyWinds/puzzle)


### Modules to be Optimised/Replaced

 - Scraper
 - Storage
 + UI will be added on

### Usage
python3 puzzle.py -i <path to original img> -d <path to where imgs are stored> -o <path to output> 


**will be modified later when the imgs from the db are integrated into the tool**


## Contributors
- [Ahn TaeGyu](https://github.com/Letm3through)

- [Fan Yuting](https://github.com/April0616)

- [Zhang Jingchen](https://github.com/jingchen-z)

- [Lucy Chan](https://github.com/lucydotc)
