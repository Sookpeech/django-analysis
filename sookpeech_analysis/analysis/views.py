from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import boto3
import json
import subprocess
from moviepy.editor import *
from .voice_analysis import main_analysis as ma_voice
from .video_analysis import main_analysis as ma_video

@method_decorator(csrf_exempt, name='dispatch')
def analysis(request, user_id, practice_id, rand, gender, pose_sensitivity, eyes_sensitivity):
    try: 
        # 1) s3에서 영상 가져온 후 mp4 저장시키기
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(name='sookpeech-wavfile')
        video_bytes = bucket.Object(f'video_{user_id}_{practice_id}_{rand}.mp4').get()['Body'].read() # bytes type

        f = open(f'./analysis/mp4s/{user_id}_{practice_id}_{rand}.mp4', "wb")
        f.write(video_bytes)
        f.close()
        # 2) 영상에서 음성 추출
        command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(f'./analysis/mp4s/{user_id}_{practice_id}_{rand}.mp4', f'./analysis/wavs/{user_id}_{practice_id}_{rand}.wav', format="wav")
        subprocess.call(command, shell=True)

        # TODO: 3) 영상 분석
        video_analysis_results = ma_video.start_analysis(user_id, practice_id, rand, pose_sensitivity, eyes_sensitivity)
        video_dict = {"video": video_analysis_results}

        # 4) 음성 분석
        voice_analysis_results = ma_voice.start_analysis(user_id, practice_id, rand, gender)
        voice_dict = {"voice": voice_analysis_results}

        # 5) Json 형태로 response
        analysis_results = dict(video_dict, **voice_dict)
        return JsonResponse((analysis_results))

        # TODO: 6) wav file, mp4 file 삭제
    except Exception as e:
        print(e)
        return JsonResponse({
            'response': 'fail to access to s3 files'
        })
