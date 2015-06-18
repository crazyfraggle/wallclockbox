import pygame
from datetime import datetime
from Numeric import array

from wallobject import WallObject
from roman import RomanNumber

fontfile = '../resources/Starcraft Normal.ttf'

class Position(object):
    def __init__(self, x=0, y=0, w=20, h=20):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.digit = None
        self.links = []

class DigitBox(WallObject):
    def __init__(self, letter, position):
        super(DigitBox, self).__init__()
        self.letter = letter
        self.position = array(position)
        self.movement = []
        self.vector = None
        self.destination = None
        self.passedtime = 0
        self.anim_time = 2000000.0

    def set_position(self, pos):
        self.position = array(pos)

    def on_init(self):
#        super(DigitBox, self).on_init()

        font = pygame.font.Font(fontfile, 20)
        self.surface = font.render(str(self.letter), True, (0, 255, 255))

    def on_loop(self, ms=0):
        if self.movement and not self.vector:
            print self.letter, "Creating vector"
            self.destination = array(self.movement.pop())
#            print self.destination, self.movement
            self.vector = self.destination - self.position
#            print self.vector
            self.passedtime = 0
        elif self.vector:
#            print ms, self.position, ((self.vector * ms) / self.anim_time)
            self.position = self.position + ((self.vector * ms) / self.anim_time)
            self.passedtime += ms
            if self.passedtime >= self.anim_time: # A second has passed
                print self.letter, "Clearing vector"
                self.position = self.destination
                self.destination = None
                self.passedtime = 0
                self.vector = None

    def on_render(self, surface=None):
        surface.blit(self.surface, self.position.tolist())

class WallClock(WallObject):
    def __init__(self):
        super(WallClock, self).__init__()

        # Hour letters
        self.hourX = [DigitBox("X", (20.0, 20.0)),
                      DigitBox("X", (20, 40))]
        self.hourV = [DigitBox("V", (40, 40))]
        self.hourI = [DigitBox("I", (60, 0)),
                      DigitBox("I", (60, 20)),
                      DigitBox("I", (60, 40))]

        self.minL = [DigitBox("L", (120, 40))]
        self.minX = [DigitBox("X", (140, 0)),
                     DigitBox("X", (140, 20)),
                     DigitBox("X", (140, 40)),
                     DigitBox("X", (140, 60))]
        self.minV = [DigitBox("V", (160, 40))]
        self.minI = [DigitBox("I", (180, 0)),
                     DigitBox("I", (180, 20)),
                     DigitBox("I", (180, 40))]

        for o in self.hourX + self.hourV + self.hourI:
            self.objects.append(o)
        for o in self.minL + self.minX + self.minV + self.minI:
            self.objects.append(o)

        self.lastHour = -1
        self.lastMin = -1


    def on_init(self):
        self.size = self.width, self.height = 400, 200
        self.surface = pygame.Surface(self.size)
        self.surface.fill([255, 0, 0])

        font = pygame.font.Font(fontfile, 20)
        self.colon = font.render(":", True, (0, 0, 0))

        pos = (100, 100)
        self.position = pygame.Rect(pos, self.size)

        super(WallClock, self).on_init()

    def calculate_moves(self):
        pass

    def on_loop(self, ms=0):
        dt = datetime.now()
        if dt.hour != self.lastHour:
            # Update hour block.
            hour = dt.hour
            if not hour: hour = 24
            s = str(RomanNumber(hour))


            # Reset letter positions
            for i in range(len(self.hourX)):
                self.hourX[i].set_position((20, 20 + (i * 20)))
            self.hourV[0].set_position((40, 40)) # Only 1
            for i in range(len(self.hourI)):
                self.hourI[i].set_position((60, (i * 20)))

            x = 0
            v = 0
            i = 0

            pos = 5 - len(s)
            for c in s:
                if c == "X":
                    self.hourX[x].movement.append([pos * 20, 100])
                    x += 1
                elif c == "V":
                    self.hourV[v].movement.append([pos * 20, 100])
                    v += 1
                elif c == "I":
                    self.hourI[i].movement.append([pos * 20, 100])
                    i += 1
                pos += 1

            self.lastHour = dt.hour

        if dt.minute != self.lastMin:
            # Update minute block.
            s = str(RomanNumber(dt.minute))

            # Reset letter positions
            self.minL[0].set_position((120, 40)) # Only 1
            for i in range(len(self.minX)):
                self.minX[i].set_position((140, (i * 20)))
            self.minV[0].set_position((160, 40)) # Only 1
            for i in range(len(self.minI)):
                self.minI[i].set_position((180, (i * 20)))

            l = 0
            x = 0
            v = 0
            i = 0

            pos = 0##7 - len(s)
            for c in s:
                if c == "L":
                    self.minL[l].movement.append([120 + (pos * 20), 100])
                    l += 1
                elif c == "X":
                    self.minX[x].movement.append([120 + (pos * 20), 100])
                    x += 1
                elif c == "V":
                    self.minV[v].movement.append([120 + (pos * 20), 100])
                    v += 1
                elif c == "I":
                    self.minI[i].movement.append([120 + (pos * 20), 100])
                    i += 1
                pos += 1

            self.lastMin = dt.minute

        # Now let the children work a little.
        super(WallClock, self).on_loop(ms=ms)


    def on_render(self, surface=None):
        self.surface.fill((255, 0, 0))
        self.surface.fill((0, 0, 0), (0, 100, 100, 20))
        self.surface.fill((0, 0, 0), (120, 100, 140, 20))
        self.surface.blit(self.colon, (105, 100))
        super(WallClock, self).on_render(surface=self.surface)
        surface.blit(self.surface, self.position)
