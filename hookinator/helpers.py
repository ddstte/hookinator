from operator import attrgetter
from typing import Any

from .constants import HOOK_MARKERS


def bind_hooks(cls: Any) -> Any:
    hooks = {k: hook_markers_getter(v) for k, v in vars(cls).items() if hasattr(v, HOOK_MARKERS)}

    for hooked_method, hooks in hooks.items():
        for hook in sorted(hooks, key=attrgetter("method_wrapper_class.__name__")):
            hook.contribute_to_class(cls, hooked_method)

    return cls


hook_markers_getter = attrgetter(HOOK_MARKERS)
hookable = bind_hooks
