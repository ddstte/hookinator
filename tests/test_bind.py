from hookinator import MethodWrapper


def test_bind_hook(saver_class, pre_save, post_save, patched_hook_method_maker, check_wrapped_method):
    test_args = ("arg",)
    test_kwargs = {"kwarg": "kwarg"}

    patched_hook_method = patched_hook_method_maker(test_args, test_kwargs)

    pre_save.bind(patched_hook_method, saver_class)
    post_save.bind(patched_hook_method, saver_class)

    noop_hooked_saver = saver_class()

    result = noop_hooked_saver.save(*test_args, **test_kwargs)

    assert result is True
    assert patched_hook_method_maker.call_counter == 2

    check_wrapped_method(saver_class.save, MethodWrapper)
