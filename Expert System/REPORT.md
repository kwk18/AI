# Отчет по лабораторной работе
## по курсу "Искусственый интеллект"

Базовая часть программы была закончена 21 марта 2021 года

### Студенты: 

| ФИО       | Роль в проекте                     | Оценка       |
|-----------|------------------------------------|--------------|
| Алексеев Павел | Формирование логики программы; Написание кода ; Составление схемы; Помощь с отчетом|          |
| Денис Син | Формирование логики программы; Написание кода ; Составление схемы; |       |
| Наталья Чурсина | Формирование базы знаний; Формирование логики программы; Написание отчетов |      |
| Валерий Анисимов| Формирование базы знаний; Формирование запросов к пользователю; Составление схемы; |          |
| Александр Марков | Формирование базы знаний; Формирование запросов к пользователю; Составление схемы; |

## Результат проверки

| Преподаватель     | Дата         |  Оценка       |
|-------------------|--------------|---------------|
| Сошников Д.В. |              |        4       |

> *Использованное представление знаний крайне бедное - ответы на вопросы напрямую сразу влияют на параметры результата. Человек рассуждает намного более сложным образом. Понравилось, что вы реализовали архитектуру и обращение в Я.Маркет за списком товаров.*

## Тема работы

Создание ИИ, который будет помогать пользователю определиться с ЭВМ и его параметрами.

## Отчет по первой встрече 

На первой встрече команды была выбрана тема работы - помощь в выборе ноутбука (далее ЭВМ). 
Для составления схемы участники команды по-отдельности составили список параметров, по которым можно выбирать ЭВМ для пользователя. Через некоторый период времени  при совместном обсуждении мы составили общий список параметров. По данному списку параметров после была составлена онтология (в приложении пдф файл).

## Концептуализация предметной области

Опишите результаты концептуализации предметной области:
 - выделенные понятия - в блоках на схеме 
 - тип получившейся онтологии - сеть
 - статические знания на схеме распологаются в прямоугольниках, а динамические в овалах
 - Схема: [ai_graph.pdf](https://github.com/MAILabs-Edu-AI/lab-expert-system-banana/files/6435234/ai_graph_final.pdf)

## Принцип реализации системы

Первым делом программа считывает список вопросов и правил из указанных файлов в settings.py. Вопросы хранятся в виде json объектов, что позваоляет изменять список вопросов динамически или использовтаь разные наборы данных без изменения кода программы. Этот объект имеет несколько полей :
- request - текст вопроса
- answers - список ответов, которые тоже являются json обхектами и содержат поля
  - answer - текст ответа
  - properties - список характеристик ЭВМ, которые дает данный ответ

Пример объекта:
```json
{
  "category": "оба",
  "request": "Доверяете ли вы онлайн-магазинам",
  "answers": [
    {
      "answer": "нет",
      "properties": [
        {
          "name": "дисковод",
          "value": "да"
        }
      ]
    },
    {
      "answer": "да",
      "properties": [
        {
          "name": "дисковод",
          "value": "нет"
        }
      ]
    }
  ]
}
```
После считывания json объектов поочередно задаются вопросы пользователю. В зависимости от ответа сохраняются определенные характеристики в финальный список параметров. Так как некоторые параметры могут повторяться,но быть с разными значениями, необходимо отфлитровать все параметры и сделать финальную выборку. В результате получается список с параметрами жалаемой ЭВМ. Ниже приведен кусок кода из класса Controller, который производит выше описанные действия:

```python
    def __get_info_from_user(self):
        computer_properties = {}
        for request in self.requests: #перебор всех вопросов из файла
            answer, answer_properties = self.__process_request(request) #получение ответа от пользователя
            computer_properties[(request.question, answer)] = [{
                "name": prop.name,
                "value": prop.value
            } for prop in answer_properties]
        return self.properties_filter.filter(computer_properties) #фильтрация повторяющихся параметров

    def __process_request(self, request): #метод задания вопроса и получения ответа
        print(request.ask()) #формирование запроса и его печать
        answer = input('Ответ: ')
        while not request.validate_answer(answer): #проверка, что полученный ответ есть среди ответов
            print(f'{colors.WARNING}' + string_values.WRONG_ANSWER + request.ask()) #если такого отета нет, просим пользователя попробовать снова
            answer = input('Ответ: ')
        return answer, request.answer_properties[answer]
```

Так как собрать актуальную базу с техникой довольно проблематично, было принято решение формировать запрос к интеренет магазину, в кчаестве которого был выбран Яндекс.Маркет, так как он имеет достаточно много параметров и их легко формировать как запрос. 
При формировании запроса параметры сопостовляются с ид фильтра и собираются в финальный запрос. После открвается браузер с моделями, подходящими под полученные параметры. Ниже приведен метод из search_models, который преобразует параметры со значениями в фильтры и собирает все фильтры вместе.

```python
def buildFilters(filtersLib, prefs):
    res = ""
    for p in prefs:
        try:
            filterId = filtersLib.FILTERS_LAPTOP[p['name']]
            filterValueDict = filtersLib.FILTERS_LAPTOP_VALUES[filterId]
            if '~' in filterValueDict:
                res += filtersLib.formatRangeFilter(filterId, p['value'])
            elif '=' in filterValueDict:
                res += filtersLib.formatPriceFilter(filterId, p['value'])
            else:
                res += filtersLib.formatFilter(filterId, filterValueDict[p['value']])  
        except:
            if debug:
                print('Не смог собрать фильтр для {}'.format(p['name']))
                print(sys.exc_info())   
    if debug:
        print(res)    
    return res
```

Для общения с пользователем программа использует стандартные методы ввода/вывода. Что бы текст лучше воспринимался он окрашивается в различные цвета. Например вот таким образом выводится вопрос и варианты ответа к нему:

```python
def ask(self):
        question = f'{"~" * 50}\n{colors.OKGREEN}{self.question}\n'
        number = 1
        for answer in self.answer_properties.keys():
            question += f'\t{number}. {answer}\n'
            number += 1
        return question
```

## Протокол работы системы

После запуска программы выводится приветственное сообщение и запускается цикл опросника. Ответ можно выбрать числом или ввести ответ словом.

![image](https://user-images.githubusercontent.com/38594574/117315570-7c5e2380-ae90-11eb-91c0-260b851b4b0d.png)
![image](https://user-images.githubusercontent.com/38594574/117315678-91d34d80-ae90-11eb-9978-db34ae9c9d25.png)

После завершения опросника будут выведены подобранные параметры:

![image](https://user-images.githubusercontent.com/38594574/117315697-97c92e80-ae90-11eb-9ff6-7c73fc33ef93.png)

После чего откроется интернет магазин с подобранными фильтрами(не реклама):

![image](https://user-images.githubusercontent.com/38594574/117316315-25a51980-ae91-11eb-9e2e-e640f1ae23c6.png)

Если выбран вариант ответа, которого нет в списке, будет выведена ошибка:

![image](https://user-images.githubusercontent.com/38594574/117316452-4c635000-ae91-11eb-8b62-8fc142ce3790.png)

Так же, если при запуске программы добавить флаг -d, будет запущен режим отладки, в котором будут выводится системные сообщения, данные json и ошибки, если такие возникают.

![image](https://user-images.githubusercontent.com/38594574/117316824-a3692500-ae91-11eb-835d-e1171e939754.png)
![image](https://user-images.githubusercontent.com/38594574/117316837-a8c66f80-ae91-11eb-81cb-0ab1ec6ed05a.png)


## Выводы

- В процессе выполнения данного проекта, каждый из нас открыл что-то новое для себя. Мы анализировали очень много информации, читали статьи на русском и на английском языках. Попутно находили разные полезные сервисы, например https://jsoneditoronline.org/. Самым интересным и трудоемким этапом был этап составления правил для нашей экспертной системы. Кроме того, мы долго разрабатывали концепцию взаимодействия с пользователем. Научились парсить данные в формате json и разбивать их на нужные блоки в коде. 
- Командная работа проходила распределенно. Мы пользовались Kanban доской в сервисе Trello, что помогало быстро и эффективно распределять задачи.
- Конечно, наша ЭС не так близка к идеальной, но мы получили ценный опыт! В будущем, мы сможем применить эти знания, участвуя в хакатонах и различных соревнованиях. 
Выражаем Вам благодарность за интересную задачу, нам очень понравилось!