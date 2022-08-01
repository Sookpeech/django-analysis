import cv2
import mediapipe as mp
import time
import numpy as np

def pose_estimation(mp4_file_path, mp4_file_title, sensitivity):
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(mp4_file_path+mp4_file_title+".mp4")
    if not cap.isOpened():
        return {
            'error': "couldn't browse mp4 video"
        }
    FPS = int(cap.get(cv2.CAP_PROP_FPS)) # 동영상의 FPS
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 전체 FRAME
    duration = frame_count/FPS # 동영상 길이
    pTime = 0

    # 자세가 바르지 않은 시간을 세는 변수
    count = 0
    # 각 제스처를 몇 초동안 했는지 세는 변수
    first_count = 0
    second_count = 0
    third_count = 0
    # 프레임 변수
    f_count = 0

    p_before = 0
    p_present = 0

    # 첫번째 제스처 flag 변수
    f_before = 0
    f_present = 0

    # 두 번째 제스처 flag 변수
    s_before = 0
    s_present = 0

    # 세 번째 제스처 flag 변수
    t_before = 0
    t_present = 0

    # 몇 번째 프레임인지 카운트
    index = 0

    start = time.time()

    before_flag = 0
    present_flag = 0

    while True:
        success, img = cap.read()

    # 원하는 프레임 단위로 cut
        cap.set(cv2.CAP_PROP_POS_FRAMES,f_count/2);
        f_count += FPS

    #     동영상이 끝나면 break
        if (np.shape(img) == ()): break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        
        if results.pose_landmarks is None: break
        
        left_shoulder = results.pose_landmarks.landmark[11]
        right_shoulder = results.pose_landmarks.landmark[12]
        
        left_wrist = results.pose_landmarks.landmark[15]
        right_wrist = results.pose_landmarks.landmark[16]
        
        left_elbow = results.pose_landmarks.landmark[13]
        right_elbow = results.pose_landmarks.landmark[14]
        
        left_hip = results.pose_landmarks.landmark[23]
        right_hip = results.pose_landmarks.landmark[24]
        
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            
            if p_before == p_present and p_present == 1:
                count += FPS/2
                
            if f_before == f_present and f_present == 1:
                first_count += FPS/2
                
            if s_before == s_present and s_present == 1:
                second_count += FPS/2
                
            if t_before == t_present and t_present == 1:
                third_count += FPS/2
            
            p_before = p_present
            f_before = f_present
            s_before = s_present
            t_before = t_present
                

    # 자세 분석
            if (abs((left_shoulder.x + right_shoulder.x) / 2 - 0.5) >= 0.1):
    #             print("몸을 화면 가운데에 맞춰주세요.")
                cv2.putText(img, "Please adjust your body to the standard.", (100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)

            if (abs(left_shoulder.y - right_shoulder.y) >= (11 - sensitivity) * 0.01):
    #             print("두 어깨의 균형이 맞지 않습니다.")
                p_present = 1
                cv2.putText(img, "The posture is not correct.", (100,100), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            else:
                p_present = 0

    # 제스처 분석
    # 손이 얼굴 위로 올라갔을 때
            if ((left_wrist.x < left_shoulder.x) and (left_wrist.x > right_shoulder.x) \
            and (left_wrist.y < left_shoulder.y)):
    #             print("1번 제스처")
                f_present = 1
                cv2.putText(img, "Please adjust your body to the standard.", (100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)

            elif ((right_wrist.x < left_shoulder.x) and (right_wrist.x > right_shoulder.x) \
            and (right_wrist.y < right_shoulder.y)):
    #             print("1번 제스처")
                f_present = 1
                cv2.putText(img, "The posture is not correct.", (100,100), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            else:
                f_present = 0
        
    # 팔짱 끼거나 한 쪽 팔을 잡았을 때, 손 맞잡을 때
            if (abs(left_wrist.x - right_shoulder.x) <= sensitivity * 0.01 or abs(left_wrist.x - right_shoulder.x) <= sensitivity * 0.01):
    #             print("2번 제스처")
                s_present = 1
                cv2.putText(img, "Please adjust your body to the standard.", (100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            else:
                s_present = 0

    # 허리에 손을 올렸을 때
            if (abs(left_wrist.x - left_hip.x) <= sensitivity * 0.01 and abs(left_wrist.y - left_shoulder.y) <= sensitivity * 0.01):
    #             print("3번 제스처")
                t_present = 1
                cv2.putText(img, "Please adjust your body to the standard.", (100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
                
            elif (abs(right_wrist.x - right_hip.x) <= sensitivity * 0.01 and abs(right_wrist.y - right_shoulder.y) <= sensitivity * 0.01):
    #             print("3번 제스처")
                t_present = 1
                cv2.putText(img, "Please adjust your body to the standard.", (100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            else:
                t_present = 0
            
            index += 1        
                
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

    #     cv2.putText(img, str(int(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
    #     cv2.namedWindow('pose', cv2.WINDOW_NORMAL)
        cv2.imshow("pose", img)
        cv2.waitKey(1)
        
        # 웹캠 이용시 q 입력하면 끔
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    end = time.time()
    cap.release()
    cv2.destroyWindow("pose")

    minutes = int(duration / 60)
    seconds = duration % 60

    print("영상 길이 : " + str(minutes) + ':' + str(seconds))
    print("분석에 걸린 시간 : ", (end - start))
    print("fps : ", FPS)

    print("자세가 기울어진 시간 : " + str(int((count/FPS)/60)) + ': ' + str((count/FPS)%60))
    print("1번 제스처 시간 : ", first_count/FPS)
    print("2번 제스처 시간 : ", second_count/FPS)
    print("3번 제스처 시간 : ", third_count/FPS)

    return {
        "total_duration": duration,
        "inclined_duration": (count/FPS)/60,
        "first_duration": first_count/FPS,
        "second_duration": second_count/FPS,
        "third_duration": third_count/FPS
    }



