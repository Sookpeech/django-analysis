import parselmouth
from parselmouth.praat import call

# measure pitch
def measurePitch(f0min, f0max, unit, wav_file_title, wav_file_path):
    print("\n")
    print(">>>> 사용자의 목소리 높낮이 변화율과 크기 변화율을 분석합니다.")
    voiceID = parselmouth.Sound(wav_file_path+wav_file_title+".wav")
    sound = parselmouth.Sound(voiceID) # read the sound
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return localShimmer, localJitter