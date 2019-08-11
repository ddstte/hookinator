from hookinator import MethodWrapper
from tests.fixtures import NoopHookedSaver


def test_noop_saver():
    noop_hooked_saver = NoopHookedSaver()

    assert not isinstance(noop_hooked_saver.save, MethodWrapper)
    assert not hasattr(noop_hooked_saver.save, "__wrapped__")
