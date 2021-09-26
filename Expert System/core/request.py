from .computer_property import ComputerProperty
from .res import colors


class Request:
    def __init__(self, category, question, answers):
        self.category = category
        self.question = question
        self.answer_properties = answers

    def __str__(self):
        return f"category = {self.category}\nquestion = {self.question}\nanswers = {self.answer_properties}"

    def __repr__(self):
        return f"category = {self.category}\nquestion = {self.question}\nanswers = {self.answer_properties}"

    def validate_answer(self, answer):
        if answer == 'exit':
            exit()
        elif answer in self.answer_properties: 
            return answer
        elif answer.isdigit() and int(answer) > 0 and int(answer) <= self.answer_properties.__len__():
            key = list(self.answer_properties)[int(answer) - 1]
            print(key)
            return key
        else:
            return ""

    def ask(self):
        question = f'{"~" * 50}\n{colors.OKGREEN}{self.question}\n'
        number = 1
        for answer in self.answer_properties.keys():
            question += f'\t{number}. {answer}\n'
            number += 1
        return question

    @staticmethod
    def from_json(json):
        answer_map = {}
        for answer in json['answers']:
            answer_map[answer['answer']] = [ComputerProperty.from_json(prop) for prop in answer['properties']]
        return Request(json['category'], json['request'], answer_map)
