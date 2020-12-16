from direct.showbase import DirectObject


class WallObject(object):
    def __init__(self):
        self.objects = []

    def on_init(self):
        for obj in self.objects:
            obj.on_init()

    def on_event(self, event):
        for obj in self.objects:
            obj.on_event(event)

    def on_loop(self, ms=0):
        for obj in self.objects:
            obj.on_loop(ms=ms)

    def on_render(self, *args, **kw):
        for obj in self.objects:
            obj.on_render(*args, **kw)

    def on_cleanup(self):
        for obj in self.objects:
            obj.on_cleanup()


class PandaWallObject(DirectObject.DirectObject):
    def __init__(self):
        self.objects = []

    def on_init(self):
        for obj in self.objects:
            obj.on_init()

    def on_event(self, event):
        for obj in self.objects:
            obj.on_event(event)

    def on_loop(self, ms=0):
        for obj in self.objects:
            obj.on_loop(ms=ms)

    def on_render(self, *args, **kw):
        for obj in self.objects:
            obj.on_render(*args, **kw)

    def on_cleanup(self):
        for obj in self.objects:
            obj.on_cleanup()
