from typing import Any, Callable, NamedTuple, Optional


class MethodWrapper:
    def __init__(self, method: Callable) -> None:
        self.pre_hooks = []
        self.post_hooks = []

        self.method: Callable = method
        self.instance: Optional[Any] = None

    def __get__(self, instance, owner) -> "MethodWrapper":
        self.instance = instance
        return self

    def add_pre(self, hooked_method: str) -> None:
        self.pre_hooks.append(hooked_method)

    def add_post(self, hooked_method: str) -> None:
        self.post_hooks.append(hooked_method)

    def __call__(self, *args, **kwargs) -> Any:
        self.run_pre_hooks(args, kwargs)
        result = self.method(self.instance, *args, **kwargs)
        self.run_post_hooks(args, kwargs)
        return result

    def run_pre_hooks(self, args: tuple, kwargs: dict) -> None:
        hook_caller = self.create_hook_caller(args, kwargs)
        for pre_hook in self.pre_hooks:
            hook_caller(pre_hook)

    def run_post_hooks(self, args: tuple, kwargs: dict) -> None:
        hook_caller = self.create_hook_caller(args, kwargs)
        for post_hook in self.post_hooks:
            hook_caller(post_hook)

    def create_hook_caller(self, args: tuple, kwargs: dict) -> Callable[[str], None]:
        def caller(hook_name: str):
            getattr(self.instance, hook_name)(args=args, kwargs=kwargs)

        return caller


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
