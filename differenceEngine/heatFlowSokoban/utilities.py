import pygame as pg
import os

BASE_IMAGE_PATH = "assets/images/"


def loadImage(path):
    img = pg.image.load(BASE_IMAGE_PATH + path).convert()
    return img


def loadImages(path):
    images = []
    for imageName in os.listdir(BASE_IMAGE_PATH + path):
        images.append(loadImage(path + "/" + imageName))
    return images
