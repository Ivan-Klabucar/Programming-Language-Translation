from Node import Node

class Foo(Node):
    def __init__(self, data):
        super().__init__(data)

    def say(self):
        print("Foo: Hej hej decko ti gay")
    
class Boo(Node):
    def __init__(self, data):
        super().__init__(data)

    def say(self):
        print("Boo: Odjebi u skokovima")

class Default(Node):
    def __init__(self, data):
        super().__init__(data)

    def say(self):
        print("Default")