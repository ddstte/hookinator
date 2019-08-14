from tests.fixtures import pre_save


def test_bind_hook():
    class Saver:
        def save(self, *args, **kwargs):
            return True

    test_args = ("arg",)
    test_kwargs = {"kwarg": "kwarg"}

    call_counter = 0

    def patched_hook_method(self, args, kwargs):
        nonlocal call_counter
        call_counter += 1

        assert args == test_args
        assert kwargs == test_kwargs

    pre_save.bind(patched_hook_method, Saver)
    noop_hooked_saver = Saver()

    result = noop_hooked_saver.save(*test_args, **test_kwargs)

    assert result is True
    assert call_counter == 1
