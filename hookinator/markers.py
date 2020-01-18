from functools import partial, wraps
from typing import Any, Callable, NoReturn

from .constants import HOOK_MARKERS
from .helpers import bind_hooks, hook_markers_getter, hookable
from .wrappers import MethodWrapper


class HookMarker:
    method_wrapper_class = MethodWrapper
    pre: bool = None

    def __init__(self, wrapped_method_name: str = None) -> None:
        if self.pre is None:
            raise AssertionError

        if wrapped_method_name is None:
            raise AssertionError

        self.wrapped_method_name = wrapped_method_name

    def __hash__(self) -> int:
        cls = type(self)
        attrs = (self.wrapped_method_name, self.pre, cls.__name__)
        key = "".join(str(attr) for attr in attrs)
        return hash(key)

    def __call__(self, method: Callable) -> Callable:
        vars(method).setdefault(HOOK_MARKERS, set())
        hook_markers_getter(method).add(self)
        return method

    def contribute_to_class(self, cls: Any, hooked_method: str) -> None:
        wrapped_method = self.set_wrapper(cls)
        add = wrapped_method.add_pre if self.pre else wrapped_method.add_post
        add(hooked_method)

    def bind(self, cls: Any, method: Callable) -> None:
        setattr(cls, method.__name__, method)
        self(method)
        bind_hooks(cls)

    def set_wrapper(self, cls: Any) -> MethodWrapper:
        method = getattr(cls, self.wrapped_method_name)
        if type(method) is self.method_wrapper_class:
            return method

        wrapped_method = self.method_wrapper_class(method)
        wraps(method)(wrapped_method)
        setattr(cls, self.wrapped_method_name, wrapped_method)
        return wrapped_method


class PreHookMarker(HookMarker):
    pre = True


class PostHookMarker(HookMarker):
    pre = False


class hook:
    def __init__(self, method: str, *, pre: bool = False, post: bool = False, wrapper=MethodWrapper) -> NoReturn:
        self.method = method
        self.pre = pre
        self.post = post
        self.method_wrapper_class = wrapper

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

    def set_wrapper(self, cls: Any) -> MethodWrapper:
        method = getattr(cls, self.method)
        if type(method) is self.method_wrapper_class:
            return method

        wrapped_method = self.method_wrapper_class(method)
        wraps(method)(wrapped_method)
        setattr(cls, self.method, wrapped_method)
        return wrapped_method

    def bind(self, method: Callable, cls: Any) -> None:
        setattr(cls, method.__name__, method)
        hookable(cls)
