# Panda Imports
from pandac.PandaModules import Point3
from direct.interval.IntervalGlobal import Sequence
from direct.task import Task
from direct.actor import Actor

from wallobject import PandaWallObject


class WOTest(PandaWallObject):
    def __init__(self, base, parent=None):
        self.anchor = base.render.attachNewNode("Anchor")
        self.anchor.reparentTo(parent)
        self.anchor.setPos(0, -40, 10)

        #Load the panda actor, and loop its animation
        self.pandaActor = Actor.Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.01, 0.01, 0.01)
        self.pandaActor.setHpr(-90, 0, 0)
        self.pandaActor.reparentTo(self.anchor)

        #Create the four lerp intervals needed to walk back and forth
        self.pandaPosInterval1 = self.pandaActor.posInterval(7, Point3(-10, 5, -15), startPos=Point3(10, 5, -15))
        self.pandaPosInterval2 = self.pandaActor.posInterval(7, Point3(10, 5, -15), startPos=Point3(-10, 5, -15))
        self.pandaHprInterval1 = self.pandaActor.hprInterval(3, Point3(90, 0, 0), startHpr=Point3(-90, 0, 0))
        self.pandaHprInterval2 = self.pandaActor.hprInterval(3, Point3(-90, 0, 0), startHpr=Point3(90, 0, 0))

        #Create and play the sequence that coordinates the intervals
        self.pandaPace = Sequence(self.pandaPosInterval1, self.pandaHprInterval1,
                             self.pandaPosInterval2, self.pandaHprInterval2, name="pandaPace")
        self.pandaPace.loop()
        self.pandaActor.loop("walk")
