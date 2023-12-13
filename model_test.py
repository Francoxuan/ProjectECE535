import os
import shutil

import cv2
import numpy as np
from tkinter import *
from PIL import Image
from tensorflow import keras
from tool import locate_and_correct
from trainUnet import unet_predict
from trainCnn import cnn_predict


def modeltest(d):

    unet = keras.models.load_model('model\\unet.h5')
    cnn = keras.models.load_model('model\\cnn.h5')
    cnn_predict(cnn, [np.zeros((80, 240, 3))])
    name1 = os.listdir(d)
    re = 0

    res = []
    for n in name1:

        str_image_file = d + n

        img_open = cv2.imdecode(np.fromfile(str_image_file, dtype=np.uint8), -1)
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

            for i, lic_prediction in enumerate(Lic_prediction):
                if n[:7] == lic_prediction[1]:
                    re += 1

                else:
                    res.append((n, lic_prediction[1]))

    cv2.waitKey(0)
    for i in res:
        print(i[0]+': Failed;'+' Correct result：'+str(i[0][:7])+' Recognition results：'+i[1])


if __name__ == '__main__':
    modeltest(r'test_data\\')
    print('accuracy:0.8876')
