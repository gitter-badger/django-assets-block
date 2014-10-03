class Stack(object):

    def __init__(self, name):
        self.name = name
        self.content = ''

    def add_content(self, content):
        self.content = self.content + content

    def get_content(self):
        return self.content

class Registry(object):
    def __init__(self):
        self.stacks = {}

    def get(self, name):
        if not name in self.stacks:
            self.stacks[name] = Stack(name)
        return self.stacks[name]