class Rule:

    def __init__(self, answers, properties):
        self.answers = answers
        self.properties = properties

    def can_apply(self, answer_properties):
        return self.__exist_answers(answer_properties)

    def apply(self):
        return self.properties

    def __exist_answers(self, answer_properties):
        for answer in self.answers:
            if (answer['question'], answer['answer']) not in answer_properties:
                return False
        return True

    def __repr__(self):
        return f'{self.answers}\n{self.properties}'

    @staticmethod
    def from_json(json):
        return Rule(json['answers'], json['properties'])
