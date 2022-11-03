from dataclasses import dataclass, field
from typing import List


@dataclass
class Stack:
    storage: List = field(default_factory=lambda: list())


def is_empty(stack: Stack):
    return not bool(len(stack.storage))


def top(stack: Stack):
    return stack.storage[-1]


def push(stack: Stack, elem):
    return Stack(storage=stack.storage + [elem])


def pop(stack: Stack):
    return Stack(storage=stack.storage[:-1])


if __name__ == '__main__':
    # Хехе прогон этой штуки не очень функциональный
    temp_stack = Stack()
    print("Is empty:", is_empty(temp_stack))
    print("Pushed back", 1)
    temp_stack = push(temp_stack, 1)
    print("Is empty:", is_empty(temp_stack))
    print("Top elem", top(temp_stack))
    print("Pushed back", 2)
    temp_stack = push(temp_stack, 2)
    print("Is empty:", is_empty(temp_stack))
    print("Top elem", top(temp_stack))
    print("Popped elem", top(temp_stack))
    temp_stack = pop(temp_stack)
    print("Popped elem", top(temp_stack))
    temp_stack = pop(temp_stack)
    print("Is empty:", is_empty(temp_stack))

    # <=> pop(pop(push(push(Stack(), 1), 2)))
