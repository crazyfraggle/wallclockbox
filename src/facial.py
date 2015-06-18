import cv



def do_canny(img, low, high, aperture):
    out = cv.CreateImage((img.width, img.height), 8, 1)
    return out


if __name__ == "__main__":
    print "we are we are"
    scale = 1.0

    def on_trackbar_change(val):
        global scale
        scale = val / 100.0

    cv.NamedWindow("Example2-in", cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow("Example2-out", cv.CV_WINDOW_AUTOSIZE)
    tb = cv.CreateTrackbar("slide", "Example2-out", 100, 100, on_trackbar_change)
    ##cap = cv.CaptureFromFile("/Store/Video/Shorts/stickfigurefight.avi")
    cap = cv.CaptureFromCAM(1)

    while True:
        frame = cv.QueryFrame(cap)
        size = cv.GetSize(frame)

        img = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
     #   print dir(frame)
     #   print dir(img)
#        cv.CvtColor(frame, frame, cv.CV_RGB2HSV)


#        print dir(frame)
#        print dir(img)
        if not frame:
            print "No frame. Stopping"
            break
        cv.ShowImage("Example2-in", frame)
        cv.Sub(frame, background, frame)
        cv.ShowImage("Example2-out", background)
        print scale
        a = cv.WaitKey(33)
        if a == 1048603:
            print "You escaped:", a
            break


