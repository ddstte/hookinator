from hookinator import HookinatorMixin, PostHookMarker, PreHookMarker

pre_save = PreHookMarker("save")
post_save = PostHookMarker("save")


class Saver:
    def save(self, *args, **kwargs):
        return True


class NoopHookedSaver(HookinatorMixin, Saver):
    pass


class HookedSaver(HookinatorMixin, Saver):
    @pre_save
    def _pre_hook(self, args, kwargs):
        pass

    @post_save
    def _post_hook(self, args, kwargs):
        pass
