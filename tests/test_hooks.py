from hookinator import MethodWrapper
from tests.fixtures import HookedSaver


def test_wrapped_method():
    noop_hooked_saver = HookedSaver()

    assert isinstance(noop_hooked_saver.save, MethodWrapper)
    assert hasattr(noop_hooked_saver.save, "__wrapped__")

    assert not isinstance(noop_hooked_saver.save.__wrapped__, MethodWrapper)
    assert noop_hooked_saver.save.__wrapped__.__name__ == noop_hooked_saver.save.__name__


def test_wrapped_method_return_response():
    noop_hooked_saver = HookedSaver()

    save_result = noop_hooked_saver.save()
    assert save_result is True


def test_hooks(monkeypatch):
    test_args = ("arg",)
    test_kwargs = {"kwarg": "kwarg"}

    noop_hooked_saver = HookedSaver()
    call_counter = 0

    # it is unbound method, therefore self not pass
    def patched_hook_method(args, kwargs):
        nonlocal call_counter
        call_counter += 1

        assert args == test_args
        assert kwargs == test_kwargs

    monkeypatch.setattr(noop_hooked_saver, "_pre_hook", patched_hook_method)
    monkeypatch.setattr(noop_hooked_saver, "_post_hook", patched_hook_method)

    noop_hooked_saver.save(*test_args, **test_kwargs)

    assert call_counter == 2
