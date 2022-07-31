from .pose_estimation import *
from .eyes_tracking import *

def start_analysis(user_id, practice_id, rand, pose_sensitivity, eyes_sensitivity):
    mp4_file_path = "./analysis/mp4s/"
    mp4_file_title = f'{user_id}_{practice_id}_{rand}'
    
    pose_result = pose_estimation(mp4_file_path, mp4_file_title, pose_sensitivity)
    eyes_result = eyes_tracking(mp4_file_path, mp4_file_title, eyes_sensitivity)

    video_result = dict(pose_result, **eyes_result)
    video_result = dict(
        {"pose": pose_result},
        **{"eyes": eyes_result}
    )
    
    return video_result

