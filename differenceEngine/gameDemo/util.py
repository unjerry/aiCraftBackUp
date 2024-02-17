import pygame as pg
import os

BASE_IMG_PATH = "./images/"


def load_image(path):
    img = pg.image.load(BASE_IMG_PATH + path).convert()
    return img


def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + "/" + img_name))
    return images
