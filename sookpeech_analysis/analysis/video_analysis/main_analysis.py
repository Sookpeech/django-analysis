import os
from .pose_estimation import *
from .eyes_tracking import *

def start_analysis(user_id, practice_id, pose_sensitivity, eyes_sensitivity):
    mp4_file_path = "./analysis/mp4s/"
    mp4_file_title = f'{user_id}_{practice_id}'
    
    print(">>>> step: 영상 분석-pose")
    pose_result = pose_estimation(mp4_file_path, mp4_file_title, pose_sensitivity)
    print(">>>> step: 영상 분석-eyes")
    eyes_result = eyes_tracking(mp4_file_path, mp4_file_title, eyes_sensitivity)

    video_result = dict(pose_result, **eyes_result)
    
    # mp4 파일 삭제
    file_path = f'{mp4_file_path}{mp4_file_title}.mp4'
    if os.path.exists(file_path):
        os.remove(file_path)

    return video_result

