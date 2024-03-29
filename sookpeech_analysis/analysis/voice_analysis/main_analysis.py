import chunk
import wave
import os
from .tone_analysis import *
from .pause_detection import *
from .voice_recognition import *
from .chars_analysis import *

def start_analysis(user_id, practice_id, gender):
    wav_file_path = "./analysis/wavs/"
    wav_file_title = f'{user_id}_{practice_id}'
    transcripts = []
    words_count = 0 # count num of characters
    closing_remark_count = 0 # count num of sentences with appropriate closing remarks

    # 1) get wav_file size
    wav_file_duration = getDurationSec(wav_file_path+wav_file_title+".wav")

    # 2) tone analysis
    if gender == "W" or gender == "w":
        shimmer, jitter = measurePitch(155, 334, "Hertz",wav_file_title, wav_file_path)
    else:
        shimmer, jitter = measurePitch(85, 196, "Hertz",wav_file_title, wav_file_path)
    
    # 3) split wav file by using pause_detection
    chunk_count = splitByPause(wav_file_path, wav_file_title) + 1

    # 4) start speech to text
    save_file_count = uploadTos3(wav_file_title, wav_file_path, chunk_count, user_id, practice_id)
    print(">>>>>>>>>>save_file_count=", save_file_count)
    transcripts = return_transcripts_async(save_file_count, wav_file_title, user_id)
    print(">>>>>>>>>>transcripts=", transcripts)

    # 5) preprocessing transcripts
    result = adjustSpacing(transcripts)
    print(">>>>>>>>>>result=", result)

    # 6) check speech speed & closing remarks
    words_count = 0 # count num of characters
    closing_remark_count = 0 # count num of sentences with appropriate closing remarks
    print("\n")
    print(">>>> 말하기 속도와 맺음말을 분석합니다.")
    print(f'>>>> length result={len(result)}')
    for i in range(len(result)):
        print(f'>>>> sentence_{i}={result[i].checked}')
        words_count += countNumOfWords(result[i].checked)
        closing_remark_count += checkClosingRemarks(result[i].checked)
    print(">>>>>>>>>>words_count=", words_count)
    print(">>>>>>>>>>closing_remark_count=", closing_remark_count)

    # 6) delete s3 files and transcribe job
    deleteTranscribeJob(wav_file_title, save_file_count)
    deleteS3WavFile(user_id)

    # 7) wav file, mp4 file 삭제
    file_path = f'{wav_file_path}{wav_file_title}'
    for i in range(chunk_count):
        if os.path.exists(f'{file_path}_{i}.wav'):
            os.remove(f'{file_path}_{i}.wav')
    os.remove(f'{file_path}.wav')

    return {
        'speed': round(words_count/(wav_file_duration/60)),
        'closing_remarks': round((closing_remark_count/chunk_count)*100, 1),
        'shimmer': round(shimmer*100, 2),
        'jitter': round(jitter*100, 2)
    } 

def getDurationSec(path):
    audio = wave.open(path)
    frames = audio.getnframes()
    rate = audio.getframerate()
    duration = frames/float(rate)
    return duration