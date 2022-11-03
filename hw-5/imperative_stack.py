class Stack:
    def __init__(self, storage):
        if storage is None:
            storage = []
        self.storage = storage

    def is_empty(self):
        return not bool(len(self.storage))

    def top(self):
        return self.storage[-1]

    def pop(self):
        self.storage.pop()

    def push(self, elem):
        return self.storage.append(elem)


if __name__ == '__main__':
    stack = Stack()
    print("Is empty:", stack.is_empty())
    print("Pushed back", 1)
    stack.push(1)
    print("Is empty:", stack.is_empty())
    print("Top elem", stack.top())
    print("Pushed back", 2)
    stack.push(2)
    print("Is empty:", stack.is_empty())
    print("Top elem", stack.top())
    print("Popped elem", stack.top())
    stack.pop()
    print("Popped elem", stack.top())
    stack.pop()
    print("Is empty:", stack.is_empty())
