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

# ! ls dogs-vs-cats/train/train

"""### Задание 2

Реализуйте глубокую нейронную сеть с как минимум тремя сверточными слоями. Какое качество классификации получено?

### Задание 3

Примените дополнение данных (_data augmentation_). Как это повлияло на качество классификатора?

### Задание 4

Поэкспериментируйте с готовыми нейронными сетями (например, _AlexNet_, _VGG16_, _Inception_ и т.п.), применив передаточное обучение. Как это повлияло на качество классификатора?

Какой максимальный результат удалось получить на сайте _Kaggle_? Почему?
"""