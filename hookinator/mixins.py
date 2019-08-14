from .helpers import bind_hooks


class HookinatorMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        bind_hooks(cls)
