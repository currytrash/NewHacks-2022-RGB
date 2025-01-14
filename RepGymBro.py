import cv2
import mediapipe as mp
import numpy as np
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


            # Curl counter logic
def workout_curls(shoulder, elbow, wrist, stage, counter) -> int:
    angle = calculate_angle(shoulder, elbow , wrist)
    if angle > 160:
        stage = "down"
    if angle < 30 and stage =='down':
        stage="up"
        counter +=1
    return stage, counter

#squats
def workout_squats(hip, knee, wrist, ankle, stage, counter) -> int:
    angle = calculate_angle(hip, knee, ankle)
    if angle > 160:
        stage = "up"
    if angle < 75 and stage == "up" :  
        stage="down"
        counter +=1
    print(angle)

#lateral raises
def workout_lat_raise(hip, shoulder, wrist, stage, counter) -> int:
    angle = calculate_angle(hip, shoulder, wrist)
    if angle > 90 and stage == "up":
        stage = "down"
        counter +=1
    if angle < 30:  
        stage="up"
    print(angle)


def workout_push_up(shoulder, elbow, wrist, stage, counter) -> int:
    angle = calculate_angle(shoulder, elbow, wrist)
    if angle < 50:
        stage = "down"
    if angle > 160 and stage =='down':
        stage="up"
        counter +=1
    print(angle)



def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 



#ASK for starting info
workout_types = ['push ups', 'squats', 'curls', 'lateral raises', 'sit ups'] 
for i in range (len(workout_types)):
    print (str(i+1) + ' ' + workout_types[i])

x = input('Select Workout: ')

workout = workout_types[int(x)-1]
print(workout)



cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0 
stage = None
delay = 0
#check whether to stop
flag = False
flag_count = 0


## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
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

            #squats
            #hip
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            Lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            Rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            Lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

            Relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            # Calculate angle
            #angle = calculate_angle(shoulder, elbow, wrist)
            #angle = calculate_angle(hip, knee, ankle)
            if delay <= 0:
                angle = calculate_angle(Lwrist, Rwrist, Lelbow)
            angle2 = calculate_angle(Lwrist, Rwrist, Lelbow)

            # Visualize angle
            cv2.putText(image, str(angle), 
                           tuple(np.multiply(hip, [640, 480]).astype(int)),  #replace hip for other First 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            
            '''
            if 85 < angle < 95 :
                flag= not flag
                delay = 50
                if flag == True:
                    flag_count+=1

            elif delay != 0:
                delay=delay - 1 
                #print(counter)

            angle = 0
            '''


        
            ######
            #pushups
            if workout == workout_types[0]:
                counter = workout_push_up(shoulder, elbow, wrist, stage, counter)
            #squats
            if workout == workout_types[1]:
                counter = workout_squats(hip, knee, wrist, stage, counter)
            #curls
            if workout == workout_types[2]:
                counter = workout_curls(shoulder, elbow, wrist, stage, counter)
            #lateral raises
            if workout == workout_types[3]
                counter = workout_lat_raise(hip, shoulder, wrist, stage, counter)
            print(counter)
            #sit ups
            if workout == workout_types[4]
                #insert sit up logic



            #curls
            '''
            angle = calculate_angle(shoulder, elbow , wrist)
            if angle > 160:
                stage = "down"
            if angle < 30 and stage =='down':
                stage="up"
                counter +=1
            print( counter)
            '''

            #Squats
            '''
            if angle > 160:
                stage = "up"
            if angle < 75 and stage == "up" :  
                stage="down"
                counter +=1
                #print(counter)            
            print(angle)
            '''

            #lateral raise
            '''
            if angle > 90 and stage == "up":
                stage = "down"
                counter +=1
            if angle < 30:  
                stage="up"
                #print(counter)            
            print(angle)
            '''
            
            ##push up logic
            '''
            if angle < 50:
                stage = "down"
              
            if angle > 160 and stage =='down':
                stage="up"
                counter +=1
                #print(counter)
            print(angle)

            Curls
            >160 resting 
            <30 +1 rep

            PushUp
            < 50 +1 rep
            > 160 resting
            angle(shoulder, elbow, wrist)

            Lateral Raise
            > 90 one rep 
            < 30 resting
            angle(hip, shoulder, wrist)

            Squats
            >160 resting
            <75 +1 rep



            '''



        except:
            pass
        
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Rep data
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



