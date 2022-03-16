import requests;
import json;

url = 'https://api.abuseipdb.com/api/v2/blacklist'

querystring = {
    'confidenceMinimum':'100', # ConfidenceScore(위협 점수)의 최소 값 지정
    'limit':'100' # 출력 개수 지정
}

headers = {
    'Accept': 'application/json',
    'Key': '8bcec6669b74ac01e487c5ce321ac376e3280ee2c2d80adcbf2f1b37a39b1233193372abdd2c23f7'
}

response = requests.request(method='GET', url=url, headers=headers, params=querystring)

decodedResponse = json.loads(response.text)

with open("C:\\Users\\KSCLOUD\\Desktop\\BOX\\abuse-ip-db-blacklist\\result.json", 'w') as outfile:
    json.dump(decodedResponse, outfile, sort_keys=True, indent=4)