class data_descriptor:
    def __init__(self, prop):
        self.prop = prop

    def __get__(self, obj, type=None):
        self.prop.instance = obj
        return self.prop(obj)

    def __set__(self, obj, value):
        self.prop.__set__(obj, value)

    def __delete__(self, obj):
        self.prop.__delete__(obj)


class non_data_descriptor:
    def __init__(self, prop):
        self.prop = prop

    def __get__(self, obj, type=None):
        return self.prop(obj)
