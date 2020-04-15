# -*- coding: utf-8 -*-
"""mo-2-2-0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LodKcNKlcSUtRLRCQPFZyYwdAiGQWFQh

# Лабораторная работа №2

## Реализация глубокой нейронной сети

В работе предлагается использовать набор данных _notMNIST_, который состоит из изображений размерностью 28×28 первых 10 букв латинского алфавита (_A_ ... _J_, соответственно). Обучающая выборка содержит порядка 500 тыс. изображений, а тестовая – около 19 тыс.

Данные можно скачать по ссылке:

* https://commondatastorage.googleapis.com/books1000/notMNIST_large.tar.gz (большой набор данных);

* https://commondatastorage.googleapis.com/books1000/notMNIST_small.tar.gz (маленький набор данных);

Описание данных на английском языке доступно по ссылке:
http://yaroslavvb.blogspot.sg/2011/09/notmnist-dataset.html

### Задание 1

Реализуйте полносвязную нейронную сеть с помощью библиотеки _TensorFlow_. В качестве алгоритма оптимизации можно использовать, например, стохастический градиент (_Stochastic Gradient Descent_, _SGD_). Определите количество скрытых слоев от 1 до 5, количество нейронов в каждом из слоев до нескольких сотен, а также их функции активации (кусочно-линейная, сигмоидная, гиперболический тангенс и т.д.).
"""

from google.colab import drive

drive.mount('/content/drive', force_remount = True)

BASE_DIR = '/content/drive/My Drive/Colab Files/mo-2'

import sys

sys.path.append(BASE_DIR)

import os

os.chdir(BASE_DIR)

import pandas as pd

dataframe = pd.read_pickle("./large.pkl")

dataframe['data'].shape

! pip install tensorflow-gpu --pre --quiet

! pip show tensorflow-gpu

import tensorflow as tf

import numpy as np

x = np.asarray(list(dataframe['data']))[..., np.newaxis]

x = tf.keras.utils.normalize(x, axis = 1)

x.shape

IMAGE_DIM_0, IMAGE_DIM_1 = x.shape[1], x.shape[2]

from tensorflow.keras.utils import to_categorical

y = to_categorical(dataframe['label'].astype('category').cat.codes.astype('int32'))

y.shape

LAYER_WIDTH = 5000

CLASSES_N = y.shape[1]

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Reshape

model = tf.keras.Sequential()

model.add(Reshape((IMAGE_DIM_0 * IMAGE_DIM_1,), input_shape = (IMAGE_DIM_0, IMAGE_DIM_1, 1)))
model.add(Dense(LAYER_WIDTH, activation = 'relu'))
model.add(Dense(LAYER_WIDTH, activation = 'sigmoid'))
model.add(Dense(LAYER_WIDTH, activation = 'tanh'))
model.add(Dense(LAYER_WIDTH, activation = 'elu'))
model.add(Dense(LAYER_WIDTH, activation = 'softmax'))
model.add(Dense(CLASSES_N))

def cat_cross_from_logits(y_true, y_pred):
    return tf.keras.losses.categorical_crossentropy(y_true, y_pred, from_logits = True)

model.compile(optimizer = 'sgd',
              loss = cat_cross_from_logits,
              metrics = ['categorical_accuracy'])

model.summary()

BATCH_SIZE = 128

r = 3608

VAL_SPLIT_RATE = 0.1

EPOCHS_N = 20

model.fit(x = x[:r * BATCH_SIZE], y = y[:r * BATCH_SIZE], epochs = EPOCHS_N, batch_size = BATCH_SIZE,
          validation_split = VAL_SPLIT_RATE)

"""### Задание 2

Как улучшилась точность классификатора по сравнению с логистической регрессией?

Стало хуже &mdash; на валидационной выборке точность составила 0. Похоже, что данная модель совершенно не подходит для решения этой задачи.

### Задание 3

Используйте регуляризацию и метод сброса нейронов (_dropout_) для борьбы с переобучением. Как улучшилось качество классификации?
"""

REG_RATE = 0.001

from tensorflow.keras.regularizers import l2

l2_reg = l2(REG_RATE)

DROPOUT_RATE = 0.2

from tensorflow.keras.layers import Dropout

dropout_layer = Dropout(DROPOUT_RATE)

model_2 = tf.keras.Sequential()

model_2.add(Reshape((IMAGE_DIM_0 * IMAGE_DIM_1,), input_shape = (IMAGE_DIM_0, IMAGE_DIM_1, 1)))
model_2.add(Dense(LAYER_WIDTH, activation = 'relu', kernel_regularizer = l2_reg))
model_2.add(dropout_layer)
model_2.add(Dense(LAYER_WIDTH, activation = 'sigmoid', kernel_regularizer = l2_reg))
model_2.add(dropout_layer)
model_2.add(Dense(LAYER_WIDTH, activation = 'tanh', kernel_regularizer = l2_reg))
model_2.add(dropout_layer)
model_2.add(Dense(LAYER_WIDTH, activation = 'sigmoid', kernel_regularizer = l2_reg))
model_2.add(dropout_layer)
model_2.add(Dense(LAYER_WIDTH, activation = 'relu', kernel_regularizer = l2_reg))
model_2.add(dropout_layer)
model_2.add(Dense(CLASSES_N))

model_2.compile(optimizer = 'sgd',
                loss = cat_cross_from_logits,
                metrics = ['categorical_accuracy'])

model_2.summary()

model_2.fit(x = x[:r * BATCH_SIZE], y = y[:r * BATCH_SIZE], epochs = EPOCHS_N, batch_size = BATCH_SIZE,
            validation_split = VAL_SPLIT_RATE)

"""Ни регуляризация, ни сброс нейронов не помогли &mdash; модель всё ещё показывает 0 точности на валидационной выборке.

### Задание 4

Воспользуйтесь динамически изменяемой скоростью обучения (_learning rate_). Наилучшая точность, достигнутая с помощью данной модели составляет 97.1%. Какую точность демонстрирует Ваша реализованная модель?
"""

from tensorflow.keras.optimizers import SGD

dyn_lr_sgd = SGD(lr = 0.01, momentum = 0.9)

model_2.compile(optimizer = dyn_lr_sgd,
                loss = cat_cross_from_logits,
                metrics = ['categorical_accuracy'])

model_2.fit(x = x[:r * BATCH_SIZE], y = y[:r * BATCH_SIZE], epochs = EPOCHS_N, batch_size = BATCH_SIZE,
            validation_split = VAL_SPLIT_RATE)

"""Динамически изменяемая скорость обучения не улучшила результат. Несмотря на то, что точность на обучающей выборке составила 81%, на валидационной по-прежнему 0%.

Можно сделать вывод, что модель с полносвязными слоями не подходит для решения задачи распознавания изображений.
"""