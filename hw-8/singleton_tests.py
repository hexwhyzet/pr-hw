import unittest

from singleton import Singleton


class Foo(metaclass=Singleton):
    pass


class Bar(metaclass=Singleton):
    pass


class TestSingleton(unittest.TestCase):

    def test_foo(self):
        f1 = Foo()
        f2 = Foo()
        assert id(f1) == id(f2)

    def test_bar(self):
        b1 = Bar()
        b2 = Bar()
        assert id(b1) == id(b2)

    def test_foo_bar(self):
        f = Foo()
        b = Bar()
        assert id(f) != id(b)


if __name__ == '__main__':
    unittest.main()
