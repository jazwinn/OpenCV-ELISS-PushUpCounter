import cv2
import DetectPosture
from ultralytics import YOLO
print("package imported")


counter = DetectPosture.Counter()
rightArm = DetectPosture.BodyCompression(
    DetectPosture.BodyKeyPoints.RIGHT_WRIST,
    DetectPosture.BodyKeyPoints.RIGHT_ELBOW,
    DetectPosture.BodyKeyPoints.RIGHT_SHOULDER
)

body = DetectPosture.BodyCompression(
    DetectPosture.BodyKeyPoints.RIGHT_SHOULDER,
    DetectPosture.BodyKeyPoints.RIGHT_HIP,
    DetectPosture.BodyKeyPoints.RIGHT_ANKLE
)

leg = DetectPosture.BodyCompression(
    DetectPosture.BodyKeyPoints.RIGHT_HIP,
    DetectPosture.BodyKeyPoints.RIGHT_KNEE,
    DetectPosture.BodyKeyPoints.RIGHT_ANKLE
)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #height
cap.set(10, 100)

model = YOLO('Resource/Models/yolo11s-pose.pt')

soundStraightenBody = None
soundStraightenLeg = None
soundBeep = None
angleWithFloor = 0

while True:
    success, img = cap.read()
    results = results = model(img)

    textColor = (255, 255, 255)
    if(rightArm.CheckStraightness(results, 30)):
        rightArm.start = True
        textColor = (0, 255, 0)
    else:
        textColor = (0, 0, 255)



    if(rightArm.TestCofidence(results) and rightArm.TestCompression(results, 40)):
        print("first stage pass!")
        # angleWithFloor = DetectPosture.AngleWithFloor(results, DetectPosture.BodyKeyPoints.RIGHT_SHOULDER,
        #                                               DetectPosture.BodyKeyPoints.RIGHT_ANKLE)
        #
        #
        # print("Angle between floor and object is: ", angleWithFloor)
        # if(angleWithFloor < 40):

        if not (body.CheckStraightness(results)):
            if (soundStraightenBody is None or not soundStraightenBody.is_alive()):
                soundStraightenBody = DetectPosture.PlaySoundAsync("Resource/Sound/straigthenbody.mp3")
        elif not (leg.CheckStraightness(results, 80)):
            if (soundStraightenLeg is None or not soundStraightenLeg.is_alive()):
                soundStraightenLeg = DetectPosture.PlaySoundAsync("Resource/Sound/straigthenbody.mp3")
        else:
            counter.value += 1
            if (soundBeep is None or not soundBeep.is_alive()):
                soundBeep = DetectPosture.PlaySoundAsync("Resource/Sound/beep.mp3")



    annotated_frame = results[0].plot()  # Draw boxes and labels
    #cv2.putText(annotated_frame, str(angleWithFloor), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, textColor, 2)
    cv2.putText(annotated_frame, str(counter.value), (50,50), cv2.FONT_HERSHEY_PLAIN, 2, textColor, 2)
    cv2.imshow("Video", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

