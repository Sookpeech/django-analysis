from hanspell import spell_checker
import urllib3
import json
from keys import ACCESS_KEY

def adjustSpacing(transcripts):
    print("\n")
    print(">>>> 음성-텍스트 변환 시 오류를 줄이기 위해 띄어쓰기 전처리를 수행합니다.")
    new_transcripts = []

    for i in range(len(transcripts)):
        new_sent = transcripts[i].replace(" ", '')
        new_transcripts.append(new_sent)

    result = spell_checker.check(new_transcripts)

    return result

def countNumOfWords(transcript):
    count = 0
    for i in range(len(transcript)):
        if transcript[i]==" ":
            count+=1
    return count+1

def checkClosingRemarks(transcript):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"
    accessKey = ACCESS_KEY
    analysisCode = "morp"
    text = transcript
    result = False

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text" : text,
            "analysis_code": analysisCode
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body = json.dumps(requestJson)
    )

    # check closing remarks are appropriate
    return_objects = json.loads(response.data)['return_object']
    sentences = return_objects["sentence"]
    morps = sentences[0]["morp"]
    for morp in morps:
        if morp["type"]=="EF" or (morp["type"]=="EC" and morp["lemma"][-1]=="요"):
            if morp["position"] >= len(text.encode())-10: #TODO: 맺음말 위치 확인
                result = True

    return result
