# Setup Flow
## Docker -> Python module -> Testing script


# For Docker setup:
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
# Python module

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

# Testing

```
python3 testing_script.py
```