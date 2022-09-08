from msilib.schema import Error
import matplotlib.pyplot as plt
import numpy as np
import boto3
import os

def draw_chart(result, user_id, practice_id, gender):
    w_min_jitter = 1.599
    w_max_jitter = 2.310
    w_min_shimmer = 7.393
    w_max_shimmer = 12.221

    m_min_jitter = 2.159
    m_max_jitter = 3.023
    m_min_shimmer = 10.132
    m_max_shimmer = 13.526

    min_speed = 96
    max_speed = 124

    font_size = 12

    # 차트 그리기
    # 1) speed
    speed_x = ['slow', 'user', 'fast']
    speed_y = [min_speed, result['voice']['speed'], max_speed]
    speed_colors = ['lightgray', 'mediumpurple', 'silver']
    plt.xlabel('standard', size=font_size)
    plt.ylabel('Words Per Minute', size=font_size)
    bar_chart=plt.bar(speed_x, speed_y, color=speed_colors)

    for rect in bar_chart:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.0, height-font_size, height, ha='center', va='bottom', size=12)
    
    plt.savefig(f'./{user_id}_{practice_id}_speed.png')
    plt.clf()

    # 2) shimmer, jitter
    if gender == 'W':
        mins = [w_min_jitter, w_min_shimmer]
        maxs = [w_max_jitter, w_max_shimmer]
    else:
        mins = [m_min_jitter, m_min_shimmer]
        maxs = [m_max_jitter, m_max_shimmer]

    users = [result['voice']['jitter'], result['voice']['shimmer']]
    checks = ['jitter', 'shimmer']

    bar_width=0.25

    index = np.arange(2)

    b1 = plt.bar(index, mins, bar_width, color='lightgray', label='mins')
    b2 = plt.bar(index+bar_width, users, bar_width, color='mediumpurple', label='users')
    b3 = plt.bar(index+2*bar_width, maxs, bar_width, color='silver', label='maxs')

    plt.legend()
    plt.savefig(f'./{user_id}_{practice_id}_shimmer_jitter.png')
    plt.clf()

    # 3) closing remarks
    closing_remark_ratio = [result['voice']['closing_remarks'], 100-result['voice']['closing_remarks']]
    closing_remark_labels = ['correctly recognized', 'recognization failed']
    closing_remark_colors = ['thistle', 'mediumpurple']
    wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

    plt.pie(closing_remark_ratio, labels=closing_remark_labels, autopct='%.1f%%', startangle=180, colors = closing_remark_colors, wedgeprops=wedgeprops)
    plt.savefig(f'./{user_id}_{practice_id}_closing_remarks.png')
    plt.clf()

    # 4) movement
    move_duration = result['video']['pose']['inclined_duration']
    +result['video']['pose']['first_duration']
    +result['video']['pose']['second_duration']
    +result['video']['pose']['third_duration']
    +result['video']['eyes']['script_duration']
    + result['video']['eyes']['around_duration'] 
    + result['video']['eyes']['face_move_duration']
    move_ratio = [result['video']['pose']['total_duration'], move_duration]
    move_labels = ['normal', 'bad movement']
    move_colors = ['thistle', 'mediumpurple']

    plt.pie(move_ratio, labels=move_labels, autopct='%.1f%%', startangle=180, colors=move_colors, wedgeprops=wedgeprops)
    plt.savefig(f'./{user_id}_{practice_id}_movement.png')
    plt.clf()

    # 5) movement detail
    bad_x = ['around', 'inclined', 'first', 'second', 'third', 'script', 'face_move']
    bad_y = [
        result['video']['eyes']['around_duration'],
        result['video']['pose']['inclined_duration'],
        result['video']['pose']['first_duration'],
        result['video']['pose']['second_duration'],
        result['video']['pose']['third_duration'],
        result['video']['eyes']['script_duration'],
        result['video']['eyes']['face_move_duration']
    ]
    bad_colors = ['thistle', 'plum', 'mediumpurple', 'mediumslateblue', 'mediumorchid', 'darkorchid', 'rebeccapurple']
    
    plt.xlabel('sort', size=font_size)
    plt.ylabel('duration', size=font_size)
    bar_chart=plt.bar(bad_x, bad_y, color=bad_colors)
    plt.savefig(f'./{user_id}_{practice_id}_movement_detail.png')
    plt.clf()

def upload_chart_to_s3(user_id, practice_id):
    s3=boto3.client('s3')
    bucket_name = "sookpeech-wavfile"

    # chart 업로드하기
    files = {
        "closing_remarks" : f'./{user_id}_{practice_id}_closing_remarks.png',
        "movement" : f'./{user_id}_{practice_id}_movement.png',
        "movement_detail": f'./{user_id}_{practice_id}_movement_detail.png',
        "shimmer_jitter" : f'./{user_id}_{practice_id}_shimmer_jitter.png',
        "speed" : f'./{user_id}_{practice_id}_speed.png'
    }

    for key in files.keys():
        try:
            file = open(files[key], 'rb')
            s3.upload_fileobj(file, bucket_name, f'{user_id}/{practice_id}/{key}.png', ExtraArgs={'ContentType': 'image/png', 'ACL':'public-read'}) 
        except:
            print(f'failed to upload chart image = {key}')


def delete_image(user_id, practice_id):
    files = {
        "closing_remarks" : f'./{user_id}_{practice_id}_closing_remarks.png',
        "movement" : f'./{user_id}_{practice_id}_movement.png',
        "movement_detail": f'./{user_id}_{practice_id}_movement_detail.png',
        "shimmer_jitter" : f'./{user_id}_{practice_id}_shimmer_jitter.png',
        "speed" : f'./{user_id}_{practice_id}_speed.png'
    }

    for key in files.keys():
        if os.path.exists(files[key]):
            os.remove(files[key])



