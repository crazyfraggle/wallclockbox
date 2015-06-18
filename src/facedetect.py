#!/bin/env python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak
"""
import sys
#from opencv.cv import *
#from opencv.highgui import *
import cv

# Global Variables
cascade = None
storage = cv.CreateMemStorage(0)
cascade_name = "../../data/haarcascades/haarcascade_frontalface_alt.xml"
input_name = "../c/lena.jpg"

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


def detect_and_draw(img):
    # allocate temporary images
    gray = cv.CreateImage((img.width, img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
			       cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

#    cv.ClearMemStorage(storage)

    if(cascade):
#        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, storage,
                                     haar_scale, min_neighbors, haar_flags)
#        t = cv.GetTickCount() - t
#        print "detection time = %gms" % (t / (cv.GetTickFrequency()*1000.))
        if faces:
            for face_rect in faces:
                rect = face_rect[0]
#                cw = self.frame_copy.width / 2.0
#                ch = self.frame_copy.height / 2.0
#                xpos = -20.0 * (rect[0] + (rect[2] / 2.0) - cw) / cw
#                zpos = -15.0 * (rect[1] + (rect[3] / 2.0) - ch) / ch
#                center = ((rect[0] + (rect[2] / 2.0) * image_scale), (rect[1] + (rect[3] / 2.0) * image_scale))
                # the input to cvHaarDetectObjects was resized, so scale the 
                # bounding box of each face and convert it to two CvPoints
                #print repr(face_rect)
                pt1 = (int(face_rect[0][0] * image_scale), int(face_rect[0][1] * image_scale))
                pt2 = (int((face_rect[0][0] + face_rect[0][2]) * image_scale),
                       int((face_rect[0][1] + face_rect[0][3]) * image_scale))
                center = ((pt2[0] - (pt2[0]-pt1[0])/2), (pt2[1] - (pt2[1]-pt1[1])/2))
                cv.Rectangle(img, pt1, pt2, cv.CV_RGB(255, 0, 0), 3, 8, 0)
                cv.Line(img, (pt1[0], center[1]), (pt2[0], center[1]), cv.CV_RGB(255, 0, 0))
                cv.Line(img, (center[0], pt1[1]), (center[0], pt2[1]), cv.CV_RGB(255, 0, 0))

    cv.ShowImage("result", img)


if __name__ == '__main__':

    if len(sys.argv) > 1:

        if sys.argv[1].startswith("--cascade="):
            cascade_name = sys.argv[1][ len("--cascade="): ]
            if len(sys.argv) > 2:
                input_name = sys.argv[2]

        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print "Usage: facedetect --cascade=\"<cascade_path>\" [filename|camera_index]\n"
            sys.exit(-1)

        else:
            input_name = sys.argv[1]

    # the OpenCV API says this function is obsolete, but we can't
    # cast the output of cvLoad to a HaarClassifierCascade, so use this anyways
    # the size parameter is ignored
    cascade = cv.Load(cascade_name)

    if not cascade:
        print "ERROR: Could not load classifier cascade"
        sys.exit(-1)

    if input_name.isdigit():
        capture = cv.CaptureFromCAM(int(input_name))
    else:
        capture = cv.CaptureFromFile(input_name)

    cv.NamedWindow("result", 1)

    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width, frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            cv.Copy(frame, frame_copy)
            detect_and_draw(frame_copy)

            if(cv.WaitKey(10) >= 0):
                break

    else:
        image = cv.LoadImage(input_name, 1)

        if image:
            detect_and_draw(image)
            cv.WaitKey(0)

    cv.DestroyWindow("result")
