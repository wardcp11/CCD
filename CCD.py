
##################################################################
#Readme First Time Setup:
#   Need to "pip install thorcam" if not installed
#   Run program once and take camID then insert below
camID = '12152'
##################################################################

import numpy as np
import time
from thorcam.camera import ThorCam

#variable to give serial connection time to initialize
sleepPeriod = 0.05

class MyThorCam(ThorCam):
    def received_camera_response(self, msg, value):
        super(MyThorCam, self).received_camera_response(msg, value)
        if msg == 'image':
            return
        print('Received "{}" with value "{}"'.format(msg, value))
    def got_image(self, image, count, queued_count, t):
        print('Received image "{}" with time "{}" and counts "{}", "{}"'
        .format(image, t, count, queued_count))


def camInit(cam):
    try:
        time.sleep(sleepPeriod)
        cam.start_cam_process()
        time.sleep(sleepPeriod)
        cam.refresh_cameras()
        time.sleep(sleepPeriod)
        if camID == '':
            print("Camera ID not setup")
            print(cam)
            return False
        else:
            print("Camera Connection Successful")
            cam.open_camera(camID)
            cam.exposure_range
            cam.exposure_ms

            #Add camera set setting to change values
            #cam.set_setting(field, value)
            cam.set_setting('exposure_ms', 150)
            return True
    except:
        print("Failed Initialization")
        return False

def takePicture(cam):
    cam.play_camera()
    time.sleep(3)
    cam.stop_playing_camera()
    cam.close_camera()
    cam.stop_cam_process(join=True)


if __name__ == '__main__':
    cam = MyThorCam()
    if camInit(cam) == False:
        print("Exiting")
    else:
        print("Success")
        takePicture(cam)
