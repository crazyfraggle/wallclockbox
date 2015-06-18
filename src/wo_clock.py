import datetime as dt

# Panda Imports
from wallobject import PandaWallObject
from direct.task import Task

class WOClock(PandaWallObject):
    def __init__(self, base, parent=None):
        self.clock = base.loader.loadModel("../resources/models/clock3")
        self.clock.reparentTo(parent)
        self.clock.setPos(-3.0, 10, 0)

        self.hours = base.loader.loadModel("../resources/models/hours")
        self.hours.reparentTo(self.clock)
        self.minutes = base.loader.loadModel("../resources/models/minutes")
        self.minutes.reparentTo(self.clock)
        self.seconds = base.loader.loadModel("../resources/models/seconds")
        self.seconds.reparentTo(self.clock)

        base.taskMgr.add(self.update_hands_task, "update_hands_task")

    def update_hands_task(self, task):
        now = dt.datetime.now()
        sec_angle = now.second * 6.0 + (6.0*now.microsecond/1000000)
        self.seconds.setHpr(0, 0, sec_angle)
        min_angle = now.minute * 6.0 + ((6.0*now.second)/60.0)
        self.minutes.setHpr(0, 0, min_angle)
        hour_angle = (now.hour%12) * 30.0 + ((30.0*now.minute)/60.0)
        self.hours.setHpr(0, 0, hour_angle)
        return Task.cont

class VetinaryClock(object):
    def __init__(self):
        pass
    
    def generate_ticks(self, ticks_per_second=5, numticks=5333):
        drift = 0
        for i in range(0,numticks):
            deviance = 1
        