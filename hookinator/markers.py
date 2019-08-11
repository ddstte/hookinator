from functools import wraps
from typing import Any, Callable

from .constants import HOOK_MARKERS
from .helpers import hook_markers_getter
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
