from inspect import isfunction


class EnumMeta(type):
    def __new__(mcs, name, bases, old_attrs):
        attrs = dict()
        for attr in old_attrs:
            if not isfunction(old_attrs[attr]):
                correct_case = attr.upper()
                if correct_case not in attrs.keys():
                    attrs[correct_case] = correct_case
        return super(EnumMeta, mcs).__new__(mcs, name, bases, attrs)


class MyEnum(metaclass=EnumMeta):
    Open = 1
    Closed = "closed"
    Trashed = None

    def test(self):
        pass


enum = MyEnum.OPEN
print(enum)
try:
    MyEnum.test()
except AttributeError:
    pass
print(MyEnum.OPEN == MyEnum.CLOSED)
print(MyEnum.TRASHED == MyEnum.TRASHED)
