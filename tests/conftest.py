import pytest

from hookinator import PostHookMarker, PreHookMarker


@pytest.fixture
def saver_class():
    class Saver:
        def save(self, *args, **kwargs):
            return True

    return Saver


@pytest.fixture
def pre_save():
    return PreHookMarker("save")


@pytest.fixture
def post_save():
    return PostHookMarker("save")


@pytest.fixture
def patched_hook_method_maker():
    def maker(test_args, test_kwargs):
        maker.call_counter = 0

        def patched_hook_method(self, args, kwargs):
            maker.call_counter += 1

            assert args == test_args
            assert kwargs == test_kwargs

        return patched_hook_method

    return maker


@pytest.fixture
def check_wrapped_method():
    def maker(method, wrapper_class):
        assert isinstance(method, wrapper_class)
        assert hasattr(method, "__wrapped__")

        assert not isinstance(method.__wrapped__, wrapper_class)
        assert not hasattr(method.__wrapped__, "__wrapped__")
        assert method.__wrapped__.__name__ == method.__name__

    return maker
