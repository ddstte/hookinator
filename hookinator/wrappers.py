from typing import Any, Callable, NamedTuple, Optional

from .descriptors import data_descriptor, non_data_descriptor


class Context(NamedTuple):
    args: tuple
    kwargs: dict
    pre: bool = False
    post: bool = False
    result: Optional[Any] = None


class Wrapper:
    def __init__(self, method: Callable) -> None:
        self.pre_hooks = []
        self.post_hooks = []

        self.method: Callable = method
        self.instance: Optional[Any] = None

    def __get__(self, instance, owner) -> "Wrapper":
        self.instance = instance
        return self

    def add_pre(self, hooked_method: str) -> None:
        self.pre_hooks.append(hooked_method)

    def add_post(self, hooked_method: str) -> None:
        self.post_hooks.append(hooked_method)

    def __call__(self, *args, **kwargs) -> Any:
        self.run_pre_hooks(context=Context(args=args, kwargs=kwargs, pre=True,))
        result = self.method(self.instance, *args, **kwargs)
        self.run_post_hooks(context=Context(args=args, kwargs=kwargs, post=True, result=result,))

        return result

    def run_pre_hooks(self, context: Context) -> None:
        hook_caller = self.create_hook_caller(context)
        for pre_hook in self.pre_hooks:
            hook_caller(pre_hook)

    def run_post_hooks(self, context: Context) -> None:
        hook_caller = self.create_hook_caller(context)
        for post_hook in self.post_hooks:
            hook_caller(post_hook)

    def create_hook_caller(self, context: Context) -> Callable[[str], None]:
        def caller(hook_name: str):
            getattr(self.instance, hook_name)(context)

        return caller

    def contribute_to_class(self, cls, method: str) -> None:
        setattr(cls, method, self)


class AttrWrapper(Wrapper):
    def __init__(self, method):
        super().__init__(lambda *_, **__: method)

    def contribute_to_class(self, cls, method):
        setattr(cls, method, non_data_descriptor(self))


class PropertyWrapper(Wrapper):
    def __init__(self, method):
        self._method = method
        super().__init__(method.__get__)

    def contribute_to_class(self, cls, method):
        setattr(cls, method, data_descriptor(self))

    def __set__(self, instance, value):
        self.run_pre_hooks(context=Context(args=(), kwargs={}, pre=True))
        self._method.__set__(self.instance, value)
        self.run_post_hooks(context=Context(args=(), kwargs={}, post=True, result=None))

    def __delete__(self, instance):
        self.run_pre_hooks(context=Context(args=(), kwargs={}, pre=True))
        self._method.__delete__(self.instance)
        self.run_post_hooks(context=Context(args=(), kwargs={}, post=True, result=None))
