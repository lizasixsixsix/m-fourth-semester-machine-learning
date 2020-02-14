# -*- coding: utf-8 -*-
"""mo-2-4-0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EtLj3M2BHBX2vNpp1CpC4UIHM2sv_S5_

# Лабораторная работа №4

## Реализация приложения по распознаванию номеров домов

Набор изображений из _Google Street View_ с изображениями номеров домов, содержащий 10 классов, соответствующих цифрам от 0 до 9.

* 73257 изображений цифр в обучающей выборке;

* 26032 изображения цифр в тестовой выборке;

* 531131 изображения, которые можно использовать как дополнение к обучающей выборке;

* В двух форматах:

    * Оригинальные изображения с выделенными цифрами;

    * Изображения размером 32×32, содержащие одну цифру;

* Данные первого формата можно скачать по ссылкам:

    * http://ufldl.stanford.edu/housenumbers/train.tar.gz (обучающая выборка);

    * http://ufldl.stanford.edu/housenumbers/test.tar.gz (тестовая выборка);

    * http://ufldl.stanford.edu/housenumbers/extra.tar.gz (дополнительные данные);

* Данные второго формата можно скачать по ссылкам:

    * http://ufldl.stanford.edu/housenumbers/train_32x32.mat (обучающая выборка);

    * http://ufldl.stanford.edu/housenumbers/test_32x32.mat (тестовая выборка);

    * http://ufldl.stanford.edu/housenumbers/extra_32x32.mat (дополнительные данные);

* Описание данных на английском языке доступно по ссылке:

    * http://ufldl.stanford.edu/housenumbers/

### Задание 1

Реализуйте глубокую нейронную сеть (полносвязную или сверточную) и обучите ее на синтетических данных (например, наборы _MNIST_ (http://yann.lecun.com/exdb/mnist/) или _notMNIST_).

Ознакомьтесь с имеющимися работами по данной тематике: англоязычная статья ( http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42241.pdf ), видео на _YouTube_ (https://www.youtube.com/watch?v=vGPI_JvLoN0).

### Задание 2

После уточнения модели на синтетических данных попробуйте обучить ее на реальных данных (набор _Google Street View_). Что изменилось в модели?

### Задание 3

Сделайте множество снимков изображений номеров домов с помощью смартфона на ОС _Android_. Также можно использовать библиотеки _OpenCV_, _Simple CV_ или _Pygame_ для обработки изображений с общедоступных камер видеонаблюдения (например, https://www.earthcam.com/).

Пример использования библиотеки _TensorFlow_ на смартфоне можете воспользоваться демонстрационным приложением от _Google_ (https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/android).

### Задание 4

Реализуйте приложение для ОС _Android_, которое может распознавать цифры в номерах домов, используя разработанный ранее классификатор. Какова доля правильных классификаций?
"""