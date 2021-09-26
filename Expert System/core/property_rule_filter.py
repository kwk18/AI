from . import settings
from .rule import Rule
import json
import os


class PropertyRuleFilter:
    def __init__(self):
        self.rules = self.parse_rules()

    def filter(self, answer_properties):
        properties = dict()
        for rule in self.rules:
            if rule.can_apply(answer_properties):
                for prop in rule.apply():
                    properties[prop['name']] = prop

        for answer, ans_properties in answer_properties.items():
            for prop in ans_properties:
                if prop['name'] not in properties:
                    properties[prop['name']] = prop
        return [{
            'name': prop['name'],
            'value': prop['value']
        } for prop in properties.values()]

    @staticmethod
    def parse_rules():
        filenameAbs = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings.RULE_FILE)
        with open(filenameAbs) as f:
            rules = json.load(f)
            return [Rule(rule['answers'], rule['properties']) for rule in rules]
