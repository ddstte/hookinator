from functools import partial, wraps
from typing import Any, Callable

from .constants import HOOK_MARKERS
from .helpers import hook_markers_getter, hookable
from .wrappers import AttrWrapper, PropertyWrapper, Wrapper


def wrapper_builder(method) -> Wrapper:
    if callable(method):
        return Wrapper

    if not hasattr(method, "__get__"):
        return AttrWrapper

    return PropertyWrapper


class hook:
    def __init__(self, method: str, *, pre: bool = False, post: bool = False, wrapper_builder=wrapper_builder) -> None:
        self.method = method
        self.pre = pre
        self.post = post
        self.wrapper_builder = wrapper_builder

    def __call__(self, function: Callable) -> Callable:
        vars(function).setdefault(HOOK_MARKERS, [])
        hook_markers_getter(function).append(self)
        function.bind = partial(self.bind, function)
        return function

    def contribute_to_class(self, cls: Any, method: str) -> None:
        wrapped_method = self.set_wrapper(cls)

        if self.pre:
            wrapped_method.add_pre(method)
        if self.post:
            wrapped_method.add_post(method)

    def set_wrapper(self, cls: Any):
        method = getattr(cls, self.method)
        wrapper_class = self.wrapper_builder(method)
        if type(method) is wrapper_class:
            return method

        wrapped_method = wrapper_class(method)
        wraps(method)(wrapped_method)
        wrapped_method.contribute_to_class(cls, self.method)
        return wrapped_method

    def bind(self, method: Callable, cls: Any) -> None:
        setattr(cls, method.__name__, method)
        hookable(cls)
