import cv2
import numpy as np

def DetectPosture(results):
    # straighten back
    if len(results) == 0 or len(results[0].keypoints.xy) == 0:
        print("No keypoints detected")
        return
    keypoints = results[0].keypoints.xy[0].cpu().numpy()
    rightWrist = np.array(keypoints[10])
    rightElbow = np.array(keypoints[8])
    rightShoulder = np.array(keypoints[6])

    ElbowToShoulder = rightElbow - rightShoulder ##for now its right elbow and right wrist
    print( "hip to Shoulder ",ElbowToShoulder)

    ElbowToWrist = rightElbow - rightWrist
    print("hip to Ankle ", ElbowToWrist)


    # Normalize vectors
    v1 = ElbowToShoulder / np.linalg.norm(ElbowToShoulder)
    v2 = ElbowToWrist / np.linalg.norm(ElbowToWrist)

    # Compute angle in degrees
    dot_product = np.dot(v1, v2)
    # Clamp to avoid numerical errors
    dot_product = np.clip(dot_product, -1.0, 1.0)
    angle_rad = np.arccos(dot_product)
    angle_deg = np.degrees(angle_rad)

    print("Angle between shoulder-hip and hip-ankle:", angle_deg)



    # for result in results:
    #     keypoints = result.keypoints  # keypoint object
    #     print("Coordinate:", keypoints.xy)  # (x, y) coordinates
    #     print("Confidence:", keypoints.conf)  # confidence scores per keypoint
