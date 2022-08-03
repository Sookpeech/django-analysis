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
def analysis(request, user_id, practice_id, gender, pose_sensitivity, eyes_sensitivity):
    try: 
        # 1) s3에서 영상 가져온 후 mp4 저장시키기
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(name='sookpeech-wavfile')
        video_bytes = bucket.Object(f'video_{user_id}_{practice_id}.mp4').get()['Body'].read() # bytes type

        f = open(f'./analysis/mp4s/{user_id}_{practice_id}.mp4', "wb")
        f.write(video_bytes)
        f.close()
        # 2) 영상에서 음성 추출
        print(">>>> step: 영상에서 음성 추출")
        command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(f'./analysis/mp4s/{user_id}_{practice_id}.mp4', f'./analysis/wavs/{user_id}_{practice_id}.wav', format="wav")
        subprocess.call(command, shell=True)

        # TODO: 3) 영상 분석
        print(">>>> step: 영상 분석")
        video_analysis_results = ma_video.start_analysis(user_id, practice_id, pose_sensitivity, eyes_sensitivity)

        # 4) 음성 분석
        print(">>>> step: 음성 분석")
        voice_analysis_results = ma_voice.start_analysis(user_id, practice_id, gender)

        # 5) Json 형태로 response
        analysis_results = dict(video_analysis_results, **voice_analysis_results)
        return JsonResponse((analysis_results))


    except Exception as e:
        print(e)
        return JsonResponse({
            'response': 'fail to access to s3 files'
        })
