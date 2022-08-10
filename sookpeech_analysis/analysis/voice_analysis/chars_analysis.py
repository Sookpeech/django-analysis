import urllib3
import json

def countNumOfWords(transcript):
    count = 0
    for i in range(len(transcript)):
        if transcript[i]==" ":
            count+=1
    return count+1

def checkClosingRemarks(transcript):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"
    accessKey = "0bb91cbb-50c3-44e6-82d0-4813ac145e65"
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
