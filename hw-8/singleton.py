class Singleton(type):
    __created_types = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__created_types.keys():
            cls.__created_types[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__created_types[cls]
