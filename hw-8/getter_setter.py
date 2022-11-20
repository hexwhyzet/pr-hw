from copy import deepcopy


class GetterSetter(type):

    @staticmethod
    def is_empty_func(func):
        def empty_func():
            pass

        return func.__code__.co_code == empty_func.__code__.co_code

    def __new__(mcs, name, bases, old_attrs):
        attrs = deepcopy(old_attrs)
        for attr, func in old_attrs.items():
            if attr.startswith("set_") or attr.startswith("get_"):
                var_name = attr[4:]

                if var_name not in attrs.keys():
                    setattr(mcs, var_name, None)

                get_method = "get_" + var_name
                if get_method not in attrs.keys() or GetterSetter.is_empty_func(attrs[get_method]):
                    attrs[get_method] = (lambda raw_var_name: lambda self: getattr(self, raw_var_name))(var_name)
                    # не знаю как тут сделать лучше, так как иначе в лямбду заносится переменная не ее значение
                    # copy и deepcopy тоже не работает по этой причине, так как лямбда lazy

                set_method = "set_" + var_name
                if set_method not in attrs.keys() or GetterSetter.is_empty_func(attrs[set_method]):
                    attrs[set_method] = (lambda raw_var_name: lambda self, value: setattr(self, raw_var_name, value))(
                        var_name)

        return super(GetterSetter, mcs).__new__(mcs, name, bases, attrs)
