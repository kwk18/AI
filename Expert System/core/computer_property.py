class ComputerProperty:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"question = {self.name}\nanswers = {self.value}"

    def __repr__(self):
        return f"question = {self.name}\nanswers = {self.value}"

    @staticmethod
    def from_json(json):
        return ComputerProperty(json['name'], json['value'])
