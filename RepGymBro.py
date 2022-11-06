import builtins
import cv2
import mediapipe as mp
import numpy as np
import json
import requests
from bs4 import BeautifulSoup

#from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from requests_html import HTMLSession



mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(1)


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def doSet(selected):
    workout = selected
    counter = 0
    stage = None
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            angle2=0
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
          
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                Lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                Rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                Lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                angle2 = calculate_angle(Lwrist, Rwrist, Lelbow)


                if workout=="curl":
                    # Calculate curlangle
                    angle = calculate_angle(shoulder, elbow, wrist)
                    print(angle)
                    # Visualize curlangle
                    cv2.putText(image, str(angle), 
                                   tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    # Curl counter logic
                    if angle > 160:
                        stage = "down"
                    if angle < 30 and stage =='down':
                        stage="up"
                        counter +=1
                        
                elif workout=="squat":
                        # Calculate curlangle
                    angle = calculate_angle(hip, knee, ankle)
                    angle_knee = calculate_angle(hip, knee, ankle)
                    knee_angle = 180-angle_knee
                

                    angle_hip = calculate_angle(shoulder, hip, knee)
                    hip_angle = 180-angle_hip
                    # Visualize curlangle
                    cv2.putText(image, str(hip_angle), 
                                   tuple(np.multiply(hip, [640, 480]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    cv2.putText(image, str(knee_angle), 
                                   tuple(np.multiply(knee, [640, 480]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    # Curl counter logic
                  





                    if angle > 160:
                        stage = "up"
                    if angle < 75 and stage == "up" :  
                        stage="down"
                        counter +=1

                elif workout=="lateral":
                        # Calculate curlangle
                    angle = calculate_angle(hip, shoulder, wrist)
                    print(angle)
                    # Visualize curlangle
                    cv2.putText(image, str(angle), 
                                   tuple(np.multiply(shoulder, [640, 480]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    # Curl counter logic
                    if angle > 100 and stage == "down":
                        stage = "up"
                        counter +=1
                    if angle < 30:  
                        stage="down"
                elif workout=="pushup":
                        # Calculate curlangle
                    angle = calculate_angle(shoulder, elbow, wrist)
                    print(angle)
                    # Visualize curlangle
                    cv2.putText(image, str(angle), 
                                   tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    # Curl counter logic
                    if angle > 160:
                        stage = "up"
                    if angle < 50 and stage =='up':
                        stage="down"
                        counter +=1
            
                        
                           
            except:
                pass
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (300,75), (245,250,16), -1)
            

            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)    
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            

            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

             # Stage data
            cv2.putText(image, 'WORKOUT', (140,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, workout, 
                        (160,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(3, 190, 252), thickness=3, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(252, 3, 132), thickness=3, circle_radius=2) 
                                     )               
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q') :
                return counter
                break

        cap.release()
        cv2.destroyAllWindows()





y = doSet("pushup")
print (y)
