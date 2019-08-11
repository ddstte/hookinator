from operator import attrgetter

from .constants import HOOK_MARKERS
from .helpers import hook_markers_getter


class HookinatorMixin:
    def __init_subclass__(cls):
        hooks = {k: hook_markers_getter(v) for k, v in vars(cls).items() if hasattr(v, HOOK_MARKERS)}

        for hooked_method, hooks in hooks.items():
            for hook in sorted(hooks, key=attrgetter("method_wrapper_class")):
                hook.contribute_to_class(cls, hooked_method)
