import cv2
import os
import time
from face_tools import get_working_camera
import numpy as np

def enroll():
    print("========================================")
    print(" OPEN-CV SFACE NEURAL NETWORK ENROLLMENT")
    print("========================================")
    print("Please look directly at the camera.")
    
    if not os.path.exists("face_detection_yunet_2023mar.onnx") or not os.path.exists("face_recognition_sface_2021dec.onnx"):
        print("[ERROR] Neural Network ONNX files not found in the directory!")
        print("Please ensure download_models.py ran successfully.")
        return
    
    detector = cv2.FaceDetectorYN.create("face_detection_yunet_2023mar.onnx", "", (320, 320))
    recognizer = cv2.FaceRecognizerSF.create("face_recognition_sface_2021dec.onnx", "")
    
    cap = get_working_camera()
    time.sleep(1)
    
    print("\n[Scanning...]")
    
    face_feature = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        detector.setInputSize((frame.shape[1], frame.shape[0]))
        _, faces = detector.detect(frame)
        
        if faces is not None and len(faces) > 0:
            face = faces[0]
            
            box = list(map(int, face[:4]))
            cv2.rectangle(frame, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected! Hold still...", (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Enrollment", frame)
            cv2.waitKey(1000) 
            
            # Align and extract features using the SFace Neural Network
            aligned_face = recognizer.alignCrop(frame, face)
            face_feature = recognizer.feature(aligned_face)
            break
            
        cv2.imshow("Enrollment", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
    if face_feature is not None:
        np.save("master_face_sface.npy", face_feature)
        print("\n[SUCCESS] Master face profile saved to 'master_face_sface.npy'!")
    else:
        print("\n[ERROR] Could not detect a face.")

if __name__ == "__main__":
    enroll()
