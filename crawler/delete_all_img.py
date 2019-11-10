#!/usr/bin/env python3
import os

def clean_img():
    path_data = "image/"
    for i in os.listdir(path_data):
        file_data = path_data + i
        if os.path.isfile(file_data) == True:
            os.remove(file_data)

if __name__ == "__main__":
    clean_img