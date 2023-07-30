import cv2
import mediapipe as mp
import numpy as np
mp_drawing=mp.solutions.drawing_utils
mp_pose=mp.solutions.pose


#defining function to calculate angke between various joints
def cal_angle(a,b,c):
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)
    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)
    if angle>180.0:
        angle=360-angle
    return angle
    

#video feed via webcam
cap=cv2.VideoCapture(0)
counter = 0 
stage = None
with mp_pose.Pose(min_detection_confidence=0.6,min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret,frame=cap.read(0)
        
        # recolor Image
        image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable=False


        #make detection
        results=pose.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        try:
            landmarks=results.pose_landmarks.landmark
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            #calculate angle
            ang=cal_angle(shoulder,elbow,wrist)
            #visualise the angle
            cv2.putText(image,str(ang),
                        tuple(np.multiply(elbow,[640,480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,[0,0,0],2,cv2.LINE_AA)
            # Curl counter logic
            if ang > 150:
                stage = "down"
            if ang < 40 and stage =='down':
                stage="up"
                counter +=1
                print(counter)
        except:
            pass
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
                    (65,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        #render detection
        mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(100,150,200),thickness=2,circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(100,150,200),thickness=2,circle_radius=2),
                                  )
        cv2.imshow("Feed",image)

        if cv2.waitKey(10) & 0xFF==ord("r"):
            break
    cap.release()
    cv2.destroyAllWindows()