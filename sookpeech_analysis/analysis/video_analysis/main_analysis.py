from .pose_estimation import *

def start_analysis(user_id, practice_id, rand, sensitivity):
    mp4_file_path = "./analysis/mp4s/"
    mp4_file_title = f'{user_id}_{practice_id}_{rand}'
    
    pose_result = pose_estimation(mp4_file_path, mp4_file_title, sensitivity)


