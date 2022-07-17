from django.shortcuts import render
import boto3
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
def analysis(request, user_id, rand):
    try: 
        # TODO: 1) s3에서 영상 가져오기
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(name='sookpeech-wavfile')
        res = bucket.Object(f'video_{user_id}_{rand}.mp4').get()
        print(res)
        # TODO: 2) 영상에서 음성 추출
        # TODO: 3) 영상 분석
        # TODO: 4) 음성 분석
        return HttpResponse(json.dumps({
            'response': 'success'
        }))
    except Exception as e:
        return HttpResponse(json.dumps({
            'response': 'fail'
        }))
