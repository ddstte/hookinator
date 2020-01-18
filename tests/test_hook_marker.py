from hookinator.helpers import hookable
from hookinator.markers import hook


def test_hook_pre_and_post():
    call = 0

    @hookable
    class MyClass:
        @hook(method="__init__", pre=True, post=True)
        def _(self, args, kwargs):
            nonlocal call
            call += 1

    MyClass()

    assert call == 2


def test_hook():
    call = 0

    @hookable
    class MyClass:
        @hook(method="__init__", pre=False, post=False)
        def _(self, args, kwargs):
            nonlocal call
            call += 1

    MyClass()

    assert call == 0


def test_hook_pre_and_post_duble():
    call = 0

    @hookable
    class MyClass:
        @hook(method="__init__", pre=True, post=True)
        @hook(method="__init__", pre=True, post=True)
        def _(self, args, kwargs):
            nonlocal call
            call += 1

    MyClass()

    assert call == 4


def test_hook_pre_and_post_bind_to_cls():
    call = 0

    @hook(method="__init__", pre=True, post=True)
    def my_test_hook(self, args, kwargs):
        nonlocal call
        call += 1

    class MyClass:
        pass

    my_test_hook.bind(MyClass)

    MyClass()

    assert call == 2
