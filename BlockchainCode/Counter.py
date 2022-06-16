# Progressive Increment
class Counter:
    def __init__(self):
        self.id = 1000

    def count(self):
        self.id += 1
        return str(self.id)