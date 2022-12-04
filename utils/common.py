import addict
import yaml
import numpy as np
import cv2 as cv
import os, shutil
import asyncio

def get_data_from_yaml(filename):
    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    data = addict.Dict(data)
    return data

def delete_after_upload(path:str, posts_id: list):
    for item in posts_id:
        shutil.rmtree(os.path.join(path, 'images', item))
        os.remove(os.path.join(path, 'text', f'{item}.txt'))

class Wotemark:
    def __init__(self, logo):
        self.logo = logo

    def scale(self, image, scale_wight):
        (image_height, image_wight) = image.shape[:2]
        new_height = int(scale_wight / image_wight * image_height)
        return cv.resize(image, (scale_wight, new_height))

    def wotermark(self, path_full, path, filename):
        wotermark = self.scale(cv.imread(f'{self.logo}', cv.IMREAD_COLOR), 150)
        (wotermark_height, wotermark_wight) = wotermark.shape[:2]
        wotermark = cv.cvtColor(wotermark, cv.COLOR_BGR2BGRA)

        image = self.scale(cv.imread(f'{path_full}', cv.IMREAD_COLOR), 1000)
        (image_height, image_wight) = image.shape[:2]
        image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)

        overlay = np.zeros((image_height, image_wight, 4), dtype='uint8')
        overlay[image_height-wotermark_height:image_height, image_wight-wotermark_wight:image_wight] = wotermark

        cv.addWeighted(overlay, 1.0, image, 1, 5, image)
        cv.imwrite(os.path.join(path, f'{filename}'), image)