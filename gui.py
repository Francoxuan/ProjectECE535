import sys
from tkinter import *
from tkinter.filedialog import askopenfilename

import cv2
import numpy as np
from PIL import Image, ImageTk
from tensorflow import keras

from tool import locate_and_correct
from trainCnn import cnn_predict
from trainUnet import unet_predict


class Window:
    def __init__(self, win, ww, wh):
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))
        self.win.title("License Plate Recognition")
        self.img_src_path = None

        Label(self.win, text='Original:', font=('微软雅黑', 8)).place(x=0, y=0)

        Label(self.win, text='Result:', font=('微软雅黑', 14)).place(x=600, y=220)

        self.can_src = Canvas(self.win, width=512, height=512, bg='white', relief='solid', borderwidth=1)
        self.can_src.place(x=50, y=0)

        self.can_pred1 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)
        self.can_pred1.place(x=710, y=200)

        self.button1 = Button(self.win, text='Select file', width=15, height=2, command=self.load_show_img)
        self.button1.place(x=580, y=wh - 140)
        self.button2 = Button(self.win, text='Recognize', width=15, height=2, command=self.display)
        self.button2.place(x=730, y=wh - 140)
        self.button3 = Button(self.win, text='clear', width=15, height=2, command=self.clear)
        self.button3.place(x=880, y=wh - 140)
        self.unet = keras.models.load_model('model\\unet.h5')
        self.cnn = keras.models.load_model('model\\cnn.h5')
        print('Starting up, please wait...')
        cnn_predict(self.cnn, [np.zeros((80, 240, 3))])
        print("Started, start identifying!")

    def load_show_img(self):
        self.clear()
        sv = StringVar()
        sv.set(askopenfilename())

        self.img_src_path = Entry(self.win, state='readonly', textvariable=sv).get()

        img_open = Image.open(self.img_src_path)
        if img_open.size[0] * img_open.size[1] > 240 * 80:
            img_open = img_open.resize((512, 512), Image.ANTIALIAS)
        self.img_Tk = ImageTk.PhotoImage(img_open)
        self.can_src.create_image(258, 258, image=self.img_Tk, anchor='center')

    def display(self):
        if self.img_src_path is None:
            self.can_pred1.create_text(32, 15, text='请选择图片', anchor='nw', font=('黑体', 28))
        else:
            img_src = cv2.imdecode(np.fromfile(self.img_src_path, dtype=np.uint8), -1)
            h, w = img_src.shape[0], img_src.shape[1]
            if h * w <= 240 * 80 and 2 <= w / h <= 5:
                lic = cv2.resize(img_src, dsize=(240, 80), interpolation=cv2.INTER_AREA)[:, :, :3]
                img_src_copy, Lic_img = img_src, [lic]
            else:
                img_src, img_mask = unet_predict(self.unet, self.img_src_path)
                img_src_copy, Lic_img = locate_and_correct(img_src,
                                                           img_mask)

            Lic_pred = cnn_predict(self.cnn, Lic_img)
            if Lic_pred:
                img = Image.fromarray(img_src_copy[:, :, ::-1])
                self.img_Tk = ImageTk.PhotoImage(img)
                self.can_src.delete('all')
                self.can_src.create_image(258, 258, image=self.img_Tk,
                                          anchor='center')
                self.lic_Tk1 = ImageTk.PhotoImage(Image.fromarray(Lic_pred[0][0][:, :, ::-1]))

                self.can_pred1.create_text(35, 15, text=Lic_pred[0][1], anchor='nw', font=('黑体', 28))

            else:
                self.can_pred1.create_text(47, 15, text='未能识别', anchor='nw', font=('黑体', 27))

    def clear(self):
        self.can_src.delete('all')
        # self.can_lic1.delete('all')
        self.can_pred1.delete('all')
        self.img_src_path = None

    @staticmethod
    def closeEvent():
        keras.backend.clear_session()
        sys.exit()


if __name__ == '__main__':
    win = Tk()
    ww = 1000
    wh = 600
    Window(win, ww, wh)
    win.protocol()
    win.mainloop()
