import cv2
import DetectPosture
from ultralytics import YOLO
print("package imported")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #height
cap.set(10, 100)

model = YOLO('Resource/Models/yolo11n-pose.pt')


while True:
    success, img = cap.read()
    results = model(img)
    DetectPosture.DetectPosture(results)
    annotated_frame = results[0].plot()  # Draw boxes and labels

    cv2.imshow("Video", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

