import requests
import json
import csv

videoNum = input('videoNum: ')
startT = float(input('startTime(float): '))
endT = float(input('endTime(float): '))

nextCursor = None
URL = 'https://api.twitch.tv/v5/videos/%s/comments?content_offset_seconds=0' % videoNum
params = {}
params['client_id'] = 'i0xz1n3g3e61fto07o9taanicb1l4x'

response = requests.get(url=URL, params=params)
response_json = json.loads(response.text)

csvFile = open('%s.csv' % videoNum, 'w', encoding='euc_kr', newline='')
csvWriter = csv.writer(csvFile)

tictoc = 1
test = 1
while True:
    recordingSuccess = False
    for i in response_json["comments"]:
        if float(i["content_offset_seconds"]) >= float(startT) and float(i["content_offset_seconds"]) <= float(endT):
            #조건을 만족해야만 기록
            try:
                csvWriter.writerow([test, str(i["content_offset_seconds"]), i["message"]["body"]])
            except UnicodeEncodeError as e:
                print("what's wrong : " + str(test))
                print(e)
        if float(i["content_offset_seconds"]) > float(endT):
            #종료
            recordingSuccess = True
            break    
        test = test + 1

    nextCursor = response_json["_next"]
    if nextCursor == None:
        #원하는 부분 캐치했으면 문구 다르게
        print("---END OF VIDEO!!!---")
        break
    elif recordingSuccess == True:
        print("---RECORDING SUCCESS---")
        break
    URL = ('https://api.twitch.tv/v5/videos/%s/comments?cursor=' % videoNum) + nextCursor
    response = requests.get(url = URL, params = params)
    response_json = json.loads(response.text)

    print("is working ... " + str(tictoc))
    tictoc = tictoc + 1
csvFile.close()      
        
###남은 수정사항###
#utf-8
#비디오 번호 받으면 제목정보 따서 csv파일 이름에 넣기        
            