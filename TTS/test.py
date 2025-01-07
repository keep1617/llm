import requests 
import json

url = "https://typecast.ai/api/speak"

payload = json.dumps({
  "actor_id": "66596219e805ae9bb7e1338c",
  "text": "안농",
  "lang": "auto",
  "tempo": 1,
  "volume": 100,
  "pitch": 0,
  "xapi_hd": True,
  "max_seconds": 60,
  "model_version": "latest",
  "xapi_audio_format": "wav"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': ''
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
      
