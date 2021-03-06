from hookinator.helpers import hookable
from hookinator.markers import hook


def test_hook_pre_and_post():
    call = 0

    @hookable
    class MyClass:
        def method(self):
            return "test"

        @hook(method="method", pre=True, post=True)
        def _(self, context):
            nonlocal call
            call += 1

    assert MyClass().method() == "test"
    assert call == 2


def test_hook_noop():
    call = 0

    @hookable
    class MyClass:
        def method(self):
            return "test"

        @hook(method="__init__", pre=False, post=False)
        def _(self, context):
            nonlocal call
            call += 1

    assert MyClass().method() == "test"
    assert call == 0


def test_hook_pre_and_post_duble():
    call = 0

    @hookable
    class MyClass:
        def method(self):
            return "test"

        @hook(method="method", pre=True, post=True)
        @hook(method="method", pre=True, post=True)
        def _(self, context):
            nonlocal call
            call += 1

    assert MyClass().method() == "test"
    assert call == 4


def test_hook_property():
    call = 0
    property_call = 0

    @hookable
    class MyClass:
        @property
        def my_property(self):
            nonlocal property_call
            property_call += 1
            return "test"

        @hook(method="my_property", pre=True, post=True)
        def my_test_hook(self, context):
            nonlocal call
            call += 1

    instance = MyClass()

    assert instance.my_property == "test"
    assert call == 2
    assert property_call == 1


def test_hook_cls_attribute():
    call = 0

    @hookable
    class MyClass:
        attribute = "test"

        @hook(method="attribute", pre=True, post=True)
        def my_test_hook(self, context):
            nonlocal call
            call += 1

    assert MyClass().attribute == "test"
    assert call == 2


def test_hook_pre_and_post_bind_to_cls():
    call = 0

    @hook(method="method", pre=True, post=True)
    def my_test_hook(self, context):
        nonlocal call
        call += 1

    class MyClass:
        def method(self):
            return "test"

    my_test_hook.bind(MyClass)

    assert MyClass().method() == "test"
    assert call == 2


def test_data_descriptor():
    call = 0

    @hookable
    class MyClass:
        def __init__(self):
            self._value = None

        @property
        def my_property(self):
            return self._value

        @my_property.setter
        def my_property(self, value):
            self._value = value

        @my_property.deleter
        def my_property(self):
            self._value = None

        @hook(method="my_property", pre=True)
        def my_hook(self, context):
            nonlocal call
            call += 1

    instance = MyClass()

    assert instance.my_property is None
    assert call == 1

    instance.my_property = 1
    assert call == 2

    assert instance.my_property == 1
    assert call == 3

    del instance.my_property
    assert call == 4

    assert instance.my_property is None
    assert call == 5
