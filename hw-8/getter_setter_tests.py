import unittest

from getter_setter import GetterSetter


class Foo(metaclass=GetterSetter):
    def set_var1(self, value):
        self.var1 = value * 10

    def get_var2(self):
        pass

    def set_var3(self, value):
        pass

    def get_var3(self):
        return self.var3 * 10


class TestGetterSetter(unittest.TestCase):
    obj: Foo

    def setUp(self):
        self.obj = Foo()

    def test_var1(self):
        assert hasattr(self.obj, "set_var1")
        assert hasattr(self.obj, "get_var1")
        self.obj.set_var1(10)
        assert self.obj.get_var1() == 100
        self.obj.set_var1(5)
        assert self.obj.get_var1() == 50

    def test_var2(self):
        assert hasattr(self.obj, "set_var2")
        assert hasattr(self.obj, "get_var2")
        self.obj.set_var2(10)
        assert self.obj.get_var2() == 10
        self.obj.set_var2(5)
        assert self.obj.get_var2() == 5

    def test_var3(self):
        assert hasattr(self.obj, "set_var3")
        assert hasattr(self.obj, "get_var3")
        self.obj.set_var3(10)
        assert self.obj.get_var3() == 100
        self.obj.set_var3(5)
        assert self.obj.get_var3() == 50


if __name__ == '__main__':
    unittest.main()
