#import direct.directbase.DirectStart
from panda3d.core import PointLight
from direct.showbase import DirectObject
from direct.task import Task
import sys
import datetime as dt

from multiprocessing import Process, Value

from wo_clock import WOClock
from wo_test import WOTest

import cv

# Avoids using the DirectStart monstrosity.
base = ShowBase.ShowBase()

box_contents = {"clock": WOClock,
                "panda": WOTest}

cascade_name = "../resources/haarcascade_mcs_eyepair_big.xml"

# Global position of camera. Should probably be a singleton object
position = (0, -50, 0)


class WallBox(DirectObject.DirectObject):
    """Being the main container for all subobjects, this also controls camera
    and all other main stuff"""

    def __init__(self, xpos, ypos, zpos):
        # Init OpenCV stuff.
        #        self.capture = None
        #        try:
        #            self.capture = cv.CaptureFromCAM(1)
        #        except:
        #            pass

        #        self.hasCamera = self.capture is not None

        # only do the rest of the OpenCV stuff if we actually got a camera.
        #        if self.hasCamera:
        #            self.cascade = cv.Load(cascade_name)
        #            self.win = cv.NamedWindow("result", 0)
        #            self.frame_copy = None
        #            self.frame = None
        #            # OpenCV Variables
        #            self.storage = cv.CreateMemStorage(0)

        #            # Parameters for haar detection
        #            # From the API:
        #            # The default parameters (scale_factor=1.1, min_neighbors=3, flags=0) are tuned
        #            # for accurate yet slow object detection. For a faster operation on real video
        #            # images the settings are:
        #            # scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
        #            # min_size=<minimum possible face size
        #            self.min_size = (20, 20)
        #            self.image_scale = 1.3
        #            self.haar_scale = 1.2
        #            self.min_neighbors = 2
        #            self.haar_flags = 0
        #            base.taskMgr.add(self.trackEyesTask, "trackEyesTask")

        # We're not using built-in mouse.
        base.disableMouse()

        # Create screen dummy path
        self.screen = base.render.attachNewNode("Screen")
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos

        # Position camera relative to screen.
        base.camera.reparentTo(self.screen)
        # Initial Lens data
        self.lens = base.camLens
        self.lens.setFilmSize(40, 30)

        # Load box and position it behind the screen
        self.box = base.loader.loadModel("../resources/models/wallbox3")
        self.box.reparentTo(self.screen)
        self.box.setScale(1, 1, 1)
        self.box.setPos(0, 10, 0)

        # Turn on the lights
        plight = PointLight('light')
        self.plnp = base.render.attachNewNode(plight)
        base.render.setLight(self.plnp)

        # Now calculate camera
#        self.calculate_camera(0, self.ypos, 0)

        # Add contents to box.
        self.children = dict()
        for name, cls in box_contents.items():
            self.children[name] = cls(base, parent=self.box)

        # Set up tasks and event handlers
#        if not self.hasCamera:
#        base.taskMgr.add(self.trackMouseTask, "trackMouseTask")
        self.accept('wheel_up', self.onWheelUp)
        self.accept('wheel_down', self.onWheelDown)
        self.accept('escape', self.shutDown)
        base.taskMgr.add(self.trackEyesFromThread, "trackEyesFromThread")

    def onWheelUp(self):
        self.ypos += 1
        if self.ypos > -20:
            self.ypos = -20
        print(self.ypos)

    def onWheelDown(self):
        self.ypos -= 1
        print(self.ypos)

    def shutDown(self):
        # We might need something like this at some point, but not yet.
        # for child in self.children.values():
        # child.on_cleanup()

        #        if self.hasCamera:
        #            cv.DestroyWindow("result")
        self.xpos.value = -10000.0
        sys.exit()

    def calculate_camera(self, x, y, z):
        base.camera.setPos(x, y, z)

        # Adjust lens details.
        distance = self.screen.getY() - y
        self.lens.setFocalLength(distance)
        self.lens.setFilmOffset(-x, -z)

    def trackMouseTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()  # get the mouse position

            # Left<->Right center = 0.
            xpos = mpos.getX()*20
            # Up<->Down, center = 0
            zpos = mpos.getY()*15

            # Stick camera for now.
            #ypos = base.camera.getY()

            self.calculate_camera(xpos, self.ypos, zpos)
        return Task.cont

    def trackEyesFromThread(self, task):
        self.calculate_camera(
            self.xpos.value, self.ypos.value, self.zpos.value)
        return Task.cont

    def trackEyesTask(self, task):
        if not self.hasCamera:
            return Task.cont

        t = dt.datetime.now()

        frame = cv.QueryFrame(self.capture)
        if not frame:
            return Task.cont

        if not self.frame_copy:
            self.frame_copy = cv.CreateImage((frame.width, frame.height),
                                             cv.IPL_DEPTH_8U, frame.nChannels)
        cv.Copy(frame, self.frame_copy)

        # allocate temporary images
        gray = cv.CreateImage(
            (self.frame_copy.width, self.frame_copy.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(self.frame_copy.width / self.image_scale),
                                    cv.Round(self.frame_copy.height / self.image_scale)), 8, 1)

        # convert color input image to grayscale
        cv.CvtColor(self.frame_copy, gray, cv.CV_BGR2GRAY)

        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

        cv.EqualizeHist(small_img, small_img)

    #    cv.ClearMemStorage(storage)

        if(self.cascade):
            faces = cv.HaarDetectObjects(small_img, self.cascade, self.storage,
                                         self.haar_scale, self.min_neighbors, self.haar_flags)
            t2 = dt.datetime.now() - t
            print("detection time = %s" % t2)
            if faces:
                rect = faces[0][0]
                cw = self.frame_copy.width / 2.0
                ch = self.frame_copy.height / 2.0
                xpos = -20.0 * (rect[0] + (rect[2] / 2.0) - cw) / cw
                zpos = -15.0 * (rect[1] + (rect[3] / 2.0) - ch) / ch

#                self.ypos = -50 + (rect[2]-150)/2
                self.ypos = -100

                print([xpos, self.ypos, zpos, cw, ch, rect])
                self.calculate_camera(xpos, self.ypos, zpos)


#                for face_rect in faces:
                # the input to cvHaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
#                    print repr(face_rect)
#                    pt1 = (int(face_rect[0][0] * self.image_scale), int(face_rect[0][1] * self.image_scale))
#                    pt2 = (int((face_rect[0][0] + face_rect[0][2]) * self.image_scale),
#                           int((face_rect[0][1] + face_rect[0][3]) * self.image_scale))
#                    cv.Rectangle(self.frame_copy, pt1, pt2, cv.CV_RGB(255, 0, 0), 3, 8, 0)

        cv.ShowImage("result", self.frame_copy)

        return Task.cont


def eyecatcher(x, y, z):
    capture = None
    try:
        capture = cv.CaptureFromCAM(1)
    except:
        return

    cascade = cv.Load(cascade_name)
    cv.NamedWindow("result", 0)
    frame_copy = None
    frame = None
    # OpenCV Variables
    storage = cv.CreateMemStorage(0)

    # Parameters for haar detection
    # From the API:
    # The default parameters (scale_factor=1.1, min_neighbors=3, flags=0) are tuned
    # for accurate yet slow object detection. For a faster operation on real video
    # images the settings are:
    # scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
    # min_size=<minimum possible face size
    min_size = (20, 20)
    image_scale = 1.3
    haar_scale = 1.2
    min_neighbors = 2
    haar_flags = 0
#        base.taskMgr.add(self.trackEyesTask, "trackEyesTask")

    while True:
        t = dt.datetime.now()

        frame = cv.QueryFrame(capture)
        if not frame:
            return Task.cont

        if not frame_copy:
            frame_copy = cv.CreateImage((frame.width, frame.height),
                                        cv.IPL_DEPTH_8U, frame.nChannels)
        cv.Copy(frame, frame_copy)

        # allocate temporary images
        gray = cv.CreateImage((frame_copy.width, frame_copy.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(frame_copy.width / image_scale),
                                    cv.Round(frame_copy.height / image_scale)), 8, 1)

        # convert color input image to grayscale
        cv.CvtColor(frame_copy, gray, cv.CV_BGR2GRAY)

        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

        cv.EqualizeHist(small_img, small_img)

    #    cv.ClearMemStorage(storage)

        if(cascade):
            faces = cv.HaarDetectObjects(small_img, cascade, storage,
                                         haar_scale, min_neighbors, haar_flags)
            t2 = dt.datetime.now() - t
            print("detection time = %s" % t2)
            if faces:
                rect = faces[0][0]
                cw = frame_copy.width / 2.0
                ch = frame_copy.height / 2.0
                xpos = -20.0 * (rect[0] + (rect[2] / 2.0) - cw) / cw
                zpos = -15.0 * (rect[1] + (rect[3] / 2.0) - ch) / ch

#                ypos = -50 + (rect[2]-150)/2
                ypos = -100

                print([xpos, ypos, zpos, cw, ch, rect])
                position = (xpos, ypos, zpos)

                # Set shared values
                if x.value == -10000.0:
                    break
                x.value = xpos
                y.value = ypos
                z.value = zpos

#                    self.calculate_camera(xpos, self.ypos, zpos)


#                for face_rect in faces:
                # the input to cvHaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
#                    print repr(face_rect)
#                    pt1 = (int(face_rect[0][0] * self.image_scale), int(face_rect[0][1] * self.image_scale))
#                    pt2 = (int((face_rect[0][0] + face_rect[0][2]) * self.image_scale),
#                           int((face_rect[0][1] + face_rect[0][3]) * self.image_scale))
#                    cv.Rectangle(self.frame_copy, pt1, pt2, cv.CV_RGB(255, 0, 0), 3, 8, 0)

        cv.ShowImage("result", frame_copy)

# Run forest! Run!
# Eyecatcher().start()
#subprocess.Popen(["./facedetect.py", "--cascade=/home/gobo/Projects/opencv-trunk/data/haarcascades/haarcascade_mcs_eyepair_big.xml", "1"])


xpos = Value('d', 0.0)
ypos = Value('d', -150.0)
zpos = Value('d', 0.0)

p = Process(target=eyecatcher, args=(xpos, ypos, zpos))
p.start()
# p.join()
h = WallBox(xpos, ypos, zpos)
base.run()
