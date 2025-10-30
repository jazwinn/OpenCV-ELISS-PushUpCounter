import numpy as np
import threading
from enum import Enum
from playsound3 import playsound
from sympy import false


class Counter:
    def __init__(self):
        self.value = 0

def PlaySoundAsync(path):
    t = threading.Thread(target=playsound, args=(path,), daemon=True)
    t.start()
    return t

class BodyKeyPoints(Enum):
    NOISE = 0
    LEFT_EYE = 1
    RIGHT_EYE = 2
    LEFT_EAR = 3
    RIGHT_EAR = 4
    LEFT_SHOULDER = 5
    RIGHT_SHOULDER = 6
    LEFT_ELBOW = 7
    RIGHT_ELBOW = 8
    LEFT_WRIST = 9
    RIGHT_WRIST = 10
    LEFT_HIP = 11
    RIGHT_HIP = 12
    LEFT_KNEE = 13
    RIGHT_KNEE = 14
    LEFT_ANKLE = 15
    RIGHT_ANKLE = 16

def GetAngleDegree(v1, v2):
    # Compute angle in degrees
    dot_product = np.dot(v1, v2)
    # Clamp to avoid numerical errors
    dot_product = np.clip(dot_product, -1.0, 1.0)
    angle_rad = np.arccos(dot_product)
    return np.degrees(angle_rad)

def AngleWithFloor(results, bodykeypoint1, bodykeypoint2):
    if len(results) == 0 or len(results[0].keypoints.xy) == 0:
        #print("No keypoints detected")
        return
    keypoints = results[0].keypoints.xy[0].cpu().numpy()

    point_top = keypoints[bodykeypoint1.value]
    point_bottom = keypoints[bodykeypoint2.value]

    body_vec = np.array(point_top) - np.array(point_bottom)
    dx, dy = body_vec
    angle_deg = np.degrees(np.arctan2(dy, dx))  # angle relative to x-axis (floor)
    return angle_deg

class BodyCompression:

    start = False

    def __init__(self, bodykeypoint1, bodykeypoint2, bodykeypoint3):
        self.frontPart = bodykeypoint1
        self.middlePart = bodykeypoint2
        self.endPart = bodykeypoint3

    def GetFrontToEndVector(self):
        return self.frontPart - self.endPart



    def GetAngle(self, keypoints):
        rightWrist = np.array(keypoints[self.frontPart.value])
        rightElbow = np.array(keypoints[self.middlePart.value])
        rightShoulder = np.array(keypoints[self.endPart.value])

        ElbowToShoulder = rightElbow - rightShoulder

        ElbowToWrist = rightElbow - rightWrist

        # Normalize vectors
        v1 = ElbowToShoulder / np.linalg.norm(ElbowToShoulder)
        v2 = ElbowToWrist / np.linalg.norm(ElbowToWrist)


        return GetAngleDegree(v1, v2)

    def TestCompression(self, results, minAngle, confidence = 90):
        if len(results) == 0 or len(results[0].keypoints.xy) == 0:
            #print("No keypoints detected")
            return False
        keypoints = results[0].keypoints.xy[0].cpu().numpy()

        angle_deg = self.GetAngle(keypoints)


        if (self.start and angle_deg - confidence < minAngle):
            self.start = False
            return True
            #print("Stop")
        return False

    def CheckStraightness(self, results, confidence = 20):
        if len(results) == 0 or len(results[0].keypoints.xy) == 0:
            #print("No keypoints detected")
            return
        keypoints = results[0].keypoints.xy[0].cpu().numpy()

        angle_deg = self.GetAngle(keypoints)

        return abs(180 - angle_deg) <= confidence

    def TestCofidence(self, results, confidence = 0.5):
        if len(results) == 0 or len(results[0].keypoints.xy) == 0:
            #print("No keypoints detected")
            return False
        confs = results[0].keypoints.conf[0].cpu().numpy()  # first person
        keypoints_to_check = {self.frontPart.value, self.middlePart.value, self.endPart.value}


        for kp in keypoints_to_check:
            if confs[kp] < confidence:
                return False

        return True

