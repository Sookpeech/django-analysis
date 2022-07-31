import cv2
from .GazeTracking.gaze_tracking import GazeTracking
import mediapipe as mp
import time
import numpy as np

def eyes_tracking(mp4_file_path, mp4_file_title, sensitivity):
    gaze = GazeTracking()

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(mp4_file_path+mp4_file_title+".mp4")
    if not cap.isOpened():
        return {
            'error': "couldn't browse mp4 video"
        }
    
    FPS = int(cap.get(cv2.CAP_PROP_FPS)) # 동영상의 fps 알아냄
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 전체 frame 알아냄
    duration = frame_count/FPS # fps와 전체 frame 수로 동영상 길이 알아냄
    pTime = 0

    # 자세가 바르지 않은 시간을 세는 변수
    count = 0
    # 각 제스처를 몇 초동안 했는지 세는 변수
    eye_count = 0 # 주변
    face_count = 0 # 얼굴
    script_count = 0 # 대본
    # 프레임 변수
    f_count = 0

    # face
    f_before = 0
    f_present = 0

    # script
    s_before = 0
    s_present = 0

    # face movement
    m_before = 0
    m_present = 0
    # 눈 깜박임 횟수 보정값
    correction = duration / 20

    start = time.time()

    while True:
        # We get a new frame from the webcam
        _, img = cap.read()
        
        # 원하는 프레임 단위로 cut
        cap.set(cv2.CAP_PROP_POS_FRAMES,f_count/2);
        # print(index)
        f_count += FPS
        
        # 동영상이 끝나면 break
        if (np.shape(img) == ()): break
            
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(img)

        new_img = gaze.annotated_frame()
        text = ""
        
        if m_before == m_present and m_present == 1:
            face_count += FPS/2
                
        if f_before == f_present and f_present == 1:
            eye_count += FPS/2
                
        if s_before == s_present and s_present == 1:
            script_count += FPS/2
                
        f_before = f_present
        s_before = s_present
        m_before = m_present

        if gaze.is_blinking():
            s_present = 1
            text = "Blinking"
        else:
            s_present = 0
            
        if gaze.is_right():
            f_present = 1
            text = "Looking right"
        elif gaze.is_left():
            f_present = 1
            text = "Looking left"
        else:
            f_present = 0
        if gaze.is_center():
            text = "Looking center"
        
        # cv2.putText(new_img, text, (10, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        # cv2.putText(new_img, "Left pupil:  " + str(left_pupil), (10, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        # cv2.putText(new_img, "Right pupil: " + str(right_pupil), (10, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        # cv2.namedWindow('Demo', cv2.WINDOW_NORMAL)
        # cv2.imshow("Demo", new_img)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        nose = results.pose_landmarks.landmark[0]
    
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

            # 얼굴 움직임 분석
            if (abs(nose.x - 0.5) >= (11 - sensitivity) * 0.1):
                m_present = 1
                print("얼굴 움직임")
                # cv2.putText(img, "Please adjust your body to the standard.", (100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            else:
                m_present = 0
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        # cv2.waitKey(1)
        
        # 웹캠 이용시 q 입력하면 끔
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
    
    end = time.time()
    cap.release()
    # cv2.destroyWindow("Demo")

    minutes = int(duration / 60)
    seconds = duration % 60

    print("영상 길이 : " + str(minutes) + ':' + str(seconds))
    print("분석에 걸린 시간 : ", (end - start))
    print("fps : ", FPS)

    if (script_count/FPS - correction > 0):
        print("시선이 분산된 시간(대본) : ", script_count/FPS - correction)
    print("시선이 분산된 시간(주변) : ", eye_count/FPS)
    print("얼굴 움직임 시간 : ", face_count/FPS)

    return {
        "script_duration": script_count/FPS - correction,
        "around_duration": eye_count/FPS,
        "face_move_duration": face_count/FPS
    }