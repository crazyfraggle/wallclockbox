import pygame
from datetime import datetime
from clock import WallClock
from wallobject import WallObject

class WallBox(WallObject):
    def __init__(self):
        super(WallBox, self).__init__()

        self._running = False
        self.size = self.height, self.width = 640, 480

        # Append objects to the wall
        self.objects.append(WallClock())
        self.lastloop = None

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        super(WallBox, self).on_init()##??surface=self._display_surface)

        self._running = True
        self.lastloop = datetime.now()

    def on_cleanup(self):
        super(WallBox, self).on_cleanup()
        pygame.quit()
        self._running = False

    def on_event(self, event):
        # Propagate event to all children
        super(WallBox, self).on_event(event)

        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYUP:
            self._running = False

    def on_loop(self, ms=0):
        now = datetime.now()
        delta = now - self.lastloop
        self.lastloop = now
        super(WallBox, self).on_loop(ms=delta.microseconds)

    def on_render(self):
        # Clear the drawing surface 
        self._display_surface.fill([192, 192, 192, 128])

        # Call render on all children.
        super(WallBox, self).on_render(surface=self._display_surface)

        pygame.display.flip()

    def run(self):
        self.on_init()

        # THE main loop
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    app = WallBox()
    app.run()
