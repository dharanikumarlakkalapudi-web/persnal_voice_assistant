import cv2
import os
import numpy as np

def get_working_camera():
    """Finds the first camera that isn't outputting a completely black screen."""
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None and np.mean(frame) > 2.0:
                return cap
            cap.release()
            
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None and np.mean(frame) > 2.0:
                return cap
            cap.release()
            
    print("[Warning] Could not find a camera with a valid picture. Defaulting to 0.")
    return cv2.VideoCapture(0)

def verify_user_face() -> bool:
    """
    Activates the webcam and uses SFace to verify the user against the master_face_sface.npy file.
    """
    if not os.path.exists("master_face_sface.npy"):
        print("[Warning] No master profile found. Please run enroll_face.py first.")
        return False
        
    if not os.path.exists("face_detection_yunet_2023mar.onnx") or not os.path.exists("face_recognition_sface_2021dec.onnx"):
        print("[Error] ONNX models not found.")
        return False
        
    master_feature = np.load("master_face_sface.npy")
    
    detector = cv2.FaceDetectorYN.create("face_detection_yunet_2023mar.onnx", "", (320, 320))
    recognizer = cv2.FaceRecognizerSF.create("face_recognition_sface_2021dec.onnx", "")
    
    cap = get_working_camera()
    print("[Scanning face with SFace Neural Network...]")
    
    authorized = False
    
    for i in range(300):
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow("JARVIS Face ID - Look at camera", frame)
        cv2.waitKey(1)
            
        detector.setInputSize((frame.shape[1], frame.shape[0]))
        _, faces = detector.detect(frame)
        
        if faces is None or len(faces) == 0:
            if i % 10 == 0:
                print(f"[Debug {i}/300] Waiting for clear face...")
            continue
            
        print(f"[Debug {i}/300] Face detected by YuNet! Comparing features...")
            
        face = faces[0]
        aligned_face = recognizer.alignCrop(frame, face)
        live_feature = recognizer.feature(aligned_face)
        
        # Compare features using Cosine Similarity. 
        # SFace recommended threshold for cosine similarity is 0.363
        score = recognizer.match(master_feature, live_feature, cv2.FaceRecognizerSF_FR_COSINE)
        
        if score >= 0.363:
            print(f"\n[Success] User verified! Similarity Score: {score:.3f}")
            authorized = True
            break
        else:
            print(f"[Debug] Face rejected. Score {score:.3f} is below threshold 0.363")
            
    cap.release()
    cv2.destroyAllWindows()
    
    if not authorized:
        print("[Failed] Could not verify user face.")
        
    return authorized

if __name__ == "__main__":
    if verify_user_face():
        print("Verification PASS")
    else:
        print("Verification FAIL")
