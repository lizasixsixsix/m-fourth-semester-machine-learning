# -*- coding: utf-8 -*-
"""mo-2-5-0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sx45nP8IHKo4tf-6iHxYPp68nGQTisCd

# Лабораторная работа №5

## Применение сверточных нейронных сетей (бинарная классификация)

Набор данных _DogsVsCats_, который состоит из изображений различной размерности, содержащих фотографии собак и кошек.

Обучающая выборка включает в себя 25 тыс. изображений (12,5 тыс. кошек: _cat.0.jpg_, ..., _cat.12499.jpg_ и 12,5 тыс. собак: _dog.0.jpg_, …, _dog.12499.jpg_), а контрольная выборка содержит 12,5 тыс. неразмеченных изображений.

Скачать данные, а также проверить качество классификатора на тестовой выборке можно на сайте _Kaggle_: https://www.kaggle.com/c/dogs-vs-cats/data

### Задание 1

Загрузите данные. Разделите исходный набор данных на обучающую, валидационную и контрольную выборки.
"""

import warnings

warnings.filterwarnings('ignore')

from google.colab import drive

drive.mount('/content/drive', force_remount = True)

BASE_DIR = '/content/drive/My Drive/Colab Files/mo-2/dogs-vs-cats'

import sys

sys.path.append(BASE_DIR)

import os

TRAIN_ARCHIVE_NAME = 'train.zip'
TEST_ARCHIVE_NAME = 'test1.zip'

LOCAL_DIR_NAME = 'dogs-vs-cats'

from zipfile import ZipFile

with ZipFile(os.path.join(BASE_DIR, TRAIN_ARCHIVE_NAME), 'r') as zip_:
    zip_.extractall(path = os.path.join(LOCAL_DIR_NAME, 'train'))

with ZipFile(os.path.join(BASE_DIR, TEST_ARCHIVE_NAME), 'r') as zip_:
    zip_.extractall(path = os.path.join(LOCAL_DIR_NAME, 'test-1'))

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

rcParams['figure.figsize'] = 8, 6

sns.set()
sns.set_palette(sns.color_palette('hls'))

def plot_accuracy(_history,
                  _train_acc_name = 'accuracy',
                  _val_acc_name = 'val_accuracy'):

    plt.plot(_history.history[_train_acc_name])
    plt.plot(_history.history[_val_acc_name])

    plt.title('Model accuracy')

    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')

    plt.legend(['Train', 'Validation'], loc = 'right')

    plt.show()

def plot_loss(_history):

    plt.plot(_history.history['loss'])
    plt.plot(_history.history['val_loss'])

    plt.title('Model loss')

    plt.ylabel('Loss')
    plt.xlabel('Epoch')

    plt.legend(['Train', 'Validation'], loc = 'right')

    plt.show()

from matplotlib.image import imread

dir_ = 'dogs-vs-cats/train/train'

for i in range(9):

    plt.subplot(330 + 1 + i)

    image_ = imread('{}/cat.{}.jpg'.format(dir_, i))

    plt.imshow(image_)
 
plt.show()

"""Изображения необходимо прирвести к одному размеру."""

NEW_IMAGE_WIDTH = 100

from os import listdir
from os.path import join
from numpy import asarray
from numpy import save
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

def dir_to_dataset(_dir_path):
	
	photos_, labels_ = [], []

	for file_ in listdir(_dir_path):

		if file_.startswith('cat'):
			label_ = 1.0
		else:
			label_ = 0.0

		photo_ = load_img(join(_dir_path, file_),
		                  target_size = (NEW_IMAGE_WIDTH, NEW_IMAGE_WIDTH))

		photo_ = img_to_array(photo_)

		photos_.append(photo_)
		labels_.append(label_)
  
	photos_norm_ = tf.keras.utils.normalize(photos_, axis = 1)

	return asarray(photos_norm_), asarray(labels_)

! pip install tensorflow-gpu --pre --quiet

import tensorflow as tf

import numpy as np

X_all, y_all = dir_to_dataset('dogs-vs-cats/train/train')

TEST_LEN_HALF = 1000

test_interval = np.r_[0:TEST_LEN_HALF, -TEST_LEN_HALF:-0]

X, y = X_all[TEST_LEN_HALF:-TEST_LEN_HALF], y_all[TEST_LEN_HALF:-TEST_LEN_HALF]
X_test, y_test = X_all[test_interval], y_all[test_interval]

print(X.shape, y.shape)
print(X_test.shape, y_test.shape)

for i in range(9):

    plt.subplot(330 + 1 + i)

    plt.imshow(X[i])
 
plt.show()

"""Выделение валидационной выборки произойдёт автоматически по параметру `validation_split` метода `model.fit()`.

### Задание 2

Реализуйте глубокую нейронную сеть с как минимум тремя сверточными слоями. Какое качество классификации получено?
"""

from tensorflow import keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

model = tf.keras.Sequential()

model.add(Conv2D(16, 3, padding = 'same', activation = 'relu',
                 input_shape = (NEW_IMAGE_WIDTH, NEW_IMAGE_WIDTH, 3)))
model.add(MaxPooling2D())
model.add(Conv2D(32, 3, padding = 'same', activation = 'relu'))
model.add(MaxPooling2D())
model.add(Conv2D(64, 3, padding = 'same', activation = 'relu'))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(512, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(optimizer = 'sgd',
              loss = 'binary_crossentropy',
              metrics = ['accuracy'])

model.summary()

history = model.fit(x = X, y = y, epochs = 20,
                    validation_split = 0.15, verbose = 0)

plot_accuracy(history)

plot_loss(history)

results = model.evaluate(X_test, y_test)

print('Test loss, test accuracy:', results)

"""Результат &mdash; 76% на тестовой выборке.

### Задание 3

Примените дополнение данных (_data augmentation_). Как это повлияло на качество классификатора?
"""

def augment_image(image):

  image = tf.image.convert_image_dtype(image, tf.float32)
  image = tf.image.resize_with_crop_or_pad(image,
                                           NEW_IMAGE_WIDTH + 40,
                                           NEW_IMAGE_WIDTH + 40)
  image = tf.image.random_crop(image,
                               size = [NEW_IMAGE_WIDTH, NEW_IMAGE_WIDTH, 3])

  return image.numpy()

X_augmented = np.zeros_like(X)

for i, img in enumerate(X):

    X_augmented[i] = augment_image(img)

X_augmented.shape

for i in range(9):

    plt.subplot(330 + 1 + i)

    plt.imshow(X_augmented[i])
 
plt.show()

y_augmented = y

history_2 = model.fit(x = X_augmented, y = y_augmented, epochs = 20,
                      validation_split = 0.15, verbose = 0)

plot_accuracy(history_2)

plot_loss(history_2)

results_2 = model.evaluate(X_test, y_test)

print('Test loss, test accuracy:', results_2)

"""После того, как сеть обучилась на тех же данных, к которым был применён data augmentation, точность предсказания даже немного уменьшилась &mdash; до 75%.

### Задание 4

Поэкспериментируйте с готовыми нейронными сетями (например, _AlexNet_, _VGG16_, _Inception_ и т.п.), применив передаточное обучение. Как это повлияло на качество классификатора?

Какой максимальный результат удалось получить на сайте _Kaggle_? Почему?
"""