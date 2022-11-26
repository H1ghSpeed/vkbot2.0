import numpy as np
import cv2 as cv
import os



def scale(image, scale_wight):
    (image_height, image_wight) = image.shape[:2]
    new_height = int(scale_wight / image_wight * image_height)
    return cv.resize(image, (scale_wight, new_height))

def watermark(path_full, path, filename):
    watemark = scale(cv.imread('logotip_mysli.png', cv.IMREAD_COLOR), 150)
    (watemark_height, watemark_wight) = watemark.shape[:2]
    watemark = cv.cvtColor(watemark, cv.COLOR_BGR2BGRA)

    image = scale(cv.imread(f'{path_full}', cv.IMREAD_COLOR), 1000)
    (image_height, image_wight) = image.shape[:2]
    image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)

    overlay = np.zeros((image_height, image_wight, 4), dtype='uint8')
    overlay[image_height-watemark_height:image_height, image_wight-watemark_wight:image_wight] = watemark

    cv.addWeighted(overlay, 1.0, image, 1, 5, image)
    cv.imwrite(os.path.join(path, f'{filename}'), image)
