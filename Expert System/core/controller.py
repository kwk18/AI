from . import settings
import os
import json
import pprint

from .request import Request
from .res import string_values
from .res import colors
from .property_rule_filter import PropertyRuleFilter


class Controller:

    def __init__(self, debug):
        self.requests = self.parse(settings.DATA_FILE)
        self.properties_filter = PropertyRuleFilter()
        self.debug = debug
        if self.debug:
            pprint.pprint(self.properties_filter.rules)

    def run(self):
        computer_properties = self.__get_info_from_user()
        if self.debug:
            pprint.pprint(computer_properties)
        return computer_properties

    def __get_info_from_user(self):
        computer_properties = {}
        for request in self.requests:
            answer, answer_properties = self.__process_request(request)
            computer_properties[(request.question, answer)] = [{
                "name": prop.name,
                "value": prop.value
            } for prop in answer_properties]
        return self.properties_filter.filter(computer_properties)

    def __process_request(self, request):
        print(request.ask())
        answer = request.validate_answer(input('Ответ: '))
        while not answer:
            print(f'{colors.WARNING}' + string_values.WRONG_ANSWER + request.ask())
            answer = request.validate_answer(input('Ответ: '))
        return answer, request.answer_properties[answer]

    @staticmethod
    def parse(filename):
        filenameAbs = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        requests = []
        with open(filenameAbs) as f:
            json_requests = json.load(f)['requests']
            for json_request in json_requests:
                requests.append(Request.from_json(json_request))
        return requests
