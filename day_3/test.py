class Parent:

    def __init__(self):
        self.say_hello()

    def say_hello(self):
        print("parent says hello")


class Child(Parent):

    def __init__(self):
        super().__init__()

    def say_hello(self):
        print("child says hello")


child = Child()
