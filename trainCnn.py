import os

import cv2
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras import layers, models

def training_vis(hist):
    loss = hist.history['loss']
    # val_loss = hist.history['val_loss']
    acc = hist.history['accuracy']  # new version => hist.history['accuracy']
    # val_acc = hist.history['val_acc']  # => hist.history['val_accuracy']

    # make a figure
    fig = plt.figure(figsize=(8, 4))
    # subplot loss
    ax1 = fig.add_subplot(121)
    ax1.plot(loss, label='train_loss')
    # ax1.plot(val_loss, label='val_loss')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.set_title('Loss on Training and Validation Data')
    ax1.legend()
    # subplot acc
    ax2 = fig.add_subplot(122)
    ax2.plot(acc, label='train_acc')
    # ax2.plot(val_acc, label='val_acc')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Accuracy  on Training and Validation Data')
    ax2.legend()
    plt.tight_layout()
    plt.show()


def train_cnn(epochs=10):
    char_dict = {"京": 0, "沪": 1, "津": 2, "渝": 3, "冀": 4, "晋": 5, "蒙": 6, "辽": 7, "吉": 8, "黑": 9, "苏": 10,
                 "浙": 11, "皖": 12, "闽": 13, "赣": 14, "鲁": 15, "豫": 16, "鄂": 17, "湘": 19, "粤": 18, "桂": 20,
                 "琼": 21, "川": 22, "贵": 23, "云": 24, "藏": 25, "陕": 26, "甘": 27, "青": 28, "宁": 29, "新": 30,
                 "0": 31, "1": 32, "2": 33, "3": 34, "4": 35, "5": 36, "6": 37, "7": 38, "8": 39, "9": 40,
                 "A": 41, "B": 42, "C": 43, "D": 44, "E": 45, "F": 46, "G": 47, "H": 48, "J": 49, "K": 50,
                 "L": 51, "M": 52, "N": 53, "P": 54, "Q": 55, "R": 56, "S": 57, "T": 58, "U": 59, "V": 60,
                 "W": 61, "X": 62, "Y": 63, "Z": 64}


    path = 'cnn_datasets/'
    pic_name = sorted(os.listdir(path))
    n = len(pic_name)
    print("There are %d data points in the dataset" % n)
    X_train, y_train = [], []
    for i in range(n):
        print("Reading image %d" % i)

        img = cv2.imdecode(np.fromfile(path + pic_name[i], dtype=np.uint8), -1)

        label = [char_dict[name] for name in pic_name[i][0:7]]
        X_train.append(img)
        y_train.append(label)
    X_train = np.array(X_train)

    y_train = [np.array(y_train)[:, i] for i in range(7)]


    Input = layers.Input((80, 240, 3))
    x = Input
    x = layers.Conv2D(filters=16, kernel_size=(3, 3), strides=1, padding='same', activation='relu')(x)
    x = layers.MaxPool2D(pool_size=(2, 2), padding='same', strides=2)(x)
    for i in range(3):
        x = layers.Conv2D(filters=32 * 2 ** i, kernel_size=(3, 3), padding='valid', activation='relu')(x)
        x = layers.Conv2D(filters=32 * 2 ** i, kernel_size=(3, 3), padding='valid', activation='relu')(x)
        x = layers.MaxPool2D(pool_size=(2, 2), padding='same', strides=2)(x)
        x = layers.Dropout(0.5)(x)
    x = layers.Flatten()(x)
    x = layers.Dropout(0.3)(x)

    Output = [layers.Dense(65, activation='softmax', name='c%d' % (i + 1))(x) for i in range(7)]
    model = models.Model(inputs=Input, outputs=Output)
    model.summary()
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])


    # Model training
    print(f"Start training CNN, {epochs} iterations in total")
    hist = model.fit(X_train, y_train, epochs=epochs)

    # Visualizing loss and accuracy during training
    training_vis(hist)

    # Saving the model
    model.save('model/c.h5')
    print('cnn.h5 saved successfully!!!')



def cnn_predict(cnn, Lic_img):
    characters = ["京", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "皖", "闽", "赣", "鲁", "豫",
                  "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "0", "1", "2",
                  "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
                  "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    Lic_prediction = []
    for lic in Lic_img:
        lic_prediction = cnn.predict(lic.reshape(1, 80, 240, 3))
        lic_prediction = np.array(lic_prediction).reshape(7, 65)
        lic_prediction_int = lic.astype(np.uint8)

        if len(lic_prediction[lic_prediction >= 0.8]) >= 4:
            chars = ''
            for arg in np.argmax(lic_prediction, axis=1):
                chars += characters[arg]

            Lic_prediction.append((lic, chars))
    return Lic_prediction
