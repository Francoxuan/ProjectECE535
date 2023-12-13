import cv2
import numpy as np
from tkinter import *
from PIL import Image
from tensorflow import keras
from tool import locate_and_correct
from trainUnet import unet_predict
from trainCnn import cnn_predict
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def detect():

    unet = keras.models.load_model('model\\unet.h5')
    cnn = keras.models.load_model('model\\cnn.h5')
    cnn_predict(cnn, [np.zeros((80, 240, 3))])
    print("have started, start recognition!")
    str_image_file = 'test_data\\TEACHER.png'
    img_open = cv2.imread(str_image_file)
    h, w = img_open.shape[0], img_open.shape[1]
    if h * w <= 240 * 80 and 2 <= w / h <= 5:
        lic = cv2.resize(img_open, dsize=(240, 80), interpolation=cv2.INTER_AREA)[:, :, :3]
        img_src_copy, Lic_img = img_open, [lic]
    else:
        img_src, img_mask = unet_predict(unet, str_image_file)
        img_src_copy, Lic_img = locate_and_correct(img_src, img_mask)
    Lic_prediction = cnn_predict(cnn, Lic_img)
    if Lic_prediction:
        img = Image.fromarray(img_src_copy[:, :, ::-1])
        cv2.imshow('plate position', img_src_copy)
        for i, lic_prediction in enumerate(Lic_prediction):
            print(lic_prediction[1])
        cv2.waitKey(0)


if __name__ == '__main__':
    detect()
