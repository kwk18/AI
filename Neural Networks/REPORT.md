# Отчет по лабораторной работе 
## по курсу "Искусственый интеллект"

## Нейросетям для распознавания изображений


### Студенты: 

| ФИО       | Роль в проекте                               | Оценка       |
|-----------|----------------------------------------------|--------------|
| Синявский Андрей | Нейросеть, подготовка отчета          |              |
| Чурсина Наталья  | Однослойная нейросеть, датасет, отчет |              |
| Макаренкова Вера | Подготовка датасета, подготовка отчета|              |

## Результат проверки

| Преподаватель     | Дата         |  Оценка       |
|-------------------|--------------|---------------|
| Сошников Д.В. |              |     3.7          |

> *Сдано с опозданием*

## Тема работы

Классификация нейросетями (однослойной, многослойной, сверточной) набора данных, состоящего из набора смайлов    :), :(, :|

## Распределение работы в команде

Мы постарались разбить обязанности поровну и делали все по шагам. В основном получилось так:
1) Синявский Андрей - обучение нейросети, общий шаблон датасета
2) Чурсина Наталья - подготовка датасета, редактирование изображений, подготовка отчета
3) Макаренкова Вера - подготовка датасета, редактирование изображений, подготовка отчета


## Подготовка данных

Сначала мы просто выписали все смайлы (каждый член команды по 300 экземпляров) на бумаге, вот примеры:
<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/andrew_neg.jpg" alt="Andrey" width="250"/>
<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/natasha_neut.png" alt ="Natasha" width="250"/>
<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/vera_pos.png" alt="Vera" width="250"/>


Подготовка датасета осуществлялась с помощью библиотеки компьютерного зрения openCV. 
Размер изображений был выставлен как 320х320, с помощью split изображения делились на 10 квадратов.
К этим выделенным квадратам были приписаны классы картинок. Данные были перемешаны и поделены на выборку 80/20.
```
 for class_ in range(len(files)):
        for file in files[class_]:
            image = cv2.imread(file)
            image = cv2.resize(image, (320, 320), interpolation=cv2.INTER_AREA)
            for i in range(0, 320, 32):
                for j in range(0, 320, 32):
                    images.append(image[i:i + 32, j:j + 32])
                    labels.append([class_])
    images = np.array(images)
    labels = np.array(labels)
    indicies = np.arange(len(labels))
    np.random.shuffle(indicies)
    images = images[indicies]
    labels = labels[indicies]
    train_ims, test_ims = np.split(images, [len(images)*8//10])
    train_lbls, test_lbls = np.split(labels, [len(images)*8//10])
```
При этом train size: 720; test size: 180.

## Загрузка данных
После подготовки данные были загружены:
```
(train_images, train_labels), (test_images, test_labels) = data([["andrew_pos.jpg", "vera_pos.png", "natasha_pos.png"],
                                                                 ["andrew_neut.jpg", "vera_neut.png", "natasha_neut.png"],
                                                                 ["andrew_neg.jpg", "vera_neg.png", "natasha_neg.png"]])
```

## Обучение нейросети

### Полносвязная однослойная сеть
Полносвязная сеть с внутренним слоем дает более высокие результаты, чем однослойная сеть. 
Полносвязный слой (Dense) и дополнительный (Flatten):
```
 self.model = keras.Sequential([
            layers.Flatten(),
            #layers.Dense(2048, activation='relu'),
            layers.Dense(3, input_shape=(32, 32, 3))
        ])
```
![One layer](https://user-images.githubusercontent.com/34220878/123181355-ced1be80-d495-11eb-9dbb-2df789a13406.png)


### Полносвязная многослойная сеть
Применены полносвязные слои (Dense) и 1 выравнивающий (Flatten):
```
 self.model = keras.Sequential([
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.Dense(256, activation='relu'),
            layers.Dense(3)
        ])
```

<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/img/pct.png" alt="pct" width="450"/>
<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/img/pct_m.png" alt="pct_matrix" width="220"/>

График обучения нейросети выглядит достаточно хорошо, полученная точность для тестовой выборки = 0.816

***Попробуем изменить число слоёв и нейронов в слоях полносвязной модели:***

```
  self.model = keras.Sequential([
            layers.Flatten(),
            #layers.Dense(2048, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(3)
        ])
```
До изменений:
<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/img/pct_old.png" alt="pct" width="400"/>


После изменений:
<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/img/pct_new.png" alt="pct" width="400"/>

При этом точность = 0.7666

### Свёрточная сеть

```
  self.model = models.Sequential()
        self.model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(64, activation='relu'))
        self.model.add(layers.Dense(3))
```

<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/img/sv.png" alt="sv" width="450"/>
<img src="https://github.com/MAILabs-Edu-AI/lab-neural-networks-vision-koshak-s-team/blob/master/img/sv_m.png" alt="sv" width="220"/>

При этом точность =  0.9944, что является достаточно высоким результатом.
## Выводы

По результатам проведенных нами тестов можно сделать вывод, что очевидным является превосходство свёрточной сети. Такая сеть учится быстрее и достигает лучших результатов. Время обучения в нашей реализации остается в рамках разумного, поскольку нами были подобраны подходящие параметры.


Что касается данных, то, конечно, обучающая выборка должна быть разнообразна. Чем больше разных экземпляров, тем лучше. Кроме того, на результаты влияет и качество написания символов (вплоть до цвета чернил).


В целом, мы можем сделать вывод, что модель, в которой правильно подобраны слои, даст лучшие результаты, чем громоздкая и неоптимизированная сеть.

Сложности, с которыми мы столкнулись во время выполнения данной ЛР, уже не кажутся препятствиями. Самым трудным было разобраться до конца с Tenserflow, много времени было потрачено на подбор параметров и тестирование. С созданием датасета не возникло особых проблем, разве что иногда линии получались немного кривыми.

Мы считаем, что к любой командной работе должен быть организованный подход. Одной из методологий эффективного взаимодействия является методология Agile, которая сейчас используется очень часто в крупных компаниях, да и не только. Наша лабораторная была разбита на мелкие задачи, которые были помещены на борду. Каждый из нас менял статус задачи, когда что-то получалось, что позволяло нам быть в курсе работы в режиме реального времени.
