from abc import ABC


class AbstractPolygon(ABC):
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class Square(AbstractPolygon, ABC):
    def __init__(self, width, height):
        assert width > 0
        assert height > 0
        assert width == height
        self.width = width
        self.height = height
        super().__init__(width, height)

    def set_side(self, side):
        self.width = side
        self.height = side

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return self.width * 2 + self.height * 2

    def __str__(self):
        print(f"Square: side={self.width}")


class Rectangle(Square, ABC):
    def __init__(self, width, height):
        super().__init__(width, width)
        assert height > 0
        self.set_height(height)

    def set_width(self, width):
        assert width > 0
        self.width = width

    def set_height(self, height):
        assert height > 0
        self.height = height

    def __str__(self):
        print(f"Rectangle: width={self.width}, height={self.height}")


def calculate_shape_area(shape: Square):
    print(f"Shape {type(shape).__name__} {shape.width}x{shape.width} area: {shape.area()}")


square = Square(2, 2)
calculate_shape_area(square)

rectangle = Rectangle(2, 2)
calculate_shape_area(rectangle)


#  Морально готов словить ноль, но принцип замещения подразумевает, в моем понимании, что любой класс потомок может
#  быть заменен без последствий своим наследником (как минимум). Однако как реализовать эту идею через наследование,
#  где старший прямоугольник, я не понимаю, ведь базово конструктор у квадрата усиливает предусловие, а по принципу
#  замещения класс потомок должен не усиливать предусловие. С изменением порядка наследования пропадает проблема
#  с set_height и set_width так как это уже становиться не легаси для квадрата-потомка, а дополнительным функционалом
#  прямоугольника-потомка.
