import requests
import time
import rospy
from std_msgs.msg import String

API_TOKEN = '__pltBHTV8h45nonMMxV6Akh63NAfaUjY5Ne5GTyZ2nu5'


class TTS:
    def __init__(self):
        self.headers = {'Authorization': f'Bearer {API_TOKEN}'}
        self.r = requests.get('https://typecast.ai/api/actor', headers=self.headers)
        self.my_actors = self.r.json()['result']
        self.my_first_actor = self.my_actors[0]
        self.my_first_actor_id = self.my_first_actor['actor_id']
       
        
        # request speech synthesis
 
        

        
        
    def get_input(self,input_text): #input 가져오기
        self.input = input_text
        self.r = requests.post('https://typecast.ai/api/speak', headers=self.headers, json={
            'text': f'{self.input}',
            'lang': 'auto',
            'actor_id': self.my_first_actor_id,
            'xapi_hd': True,
            'model_version': 'latest'
        })
        self.speak_url = self.r.json()['result']['speak_v2_url']
        
        
    def get_output(self): #get response
        self.r = requests.get(self.speak_url, headers=self.headers)
        self.ret = self.r.json()['result']
        for _ in range(120):
            self.r = requests.get(self.speak_url, headers=self.headers)
            self.ret = self.r.json()['result']
            # audio is ready
            if self.ret['status'] == 'done':
                # download audio file
                r = requests.get(self.ret['audio_download_url'])
                
                ##save as mp3 file
                with open('여자아나운서.mp3', 'wb') as f:
                    f.write(r.content)
                break
            else:
                print(f"status: {self.ret['status']}, waiting 1 second")
                time.sleep(1)
        
        
        
        


    





if __name__ == "__main__":
    tts_client = TTS()
    tts_client.get_input('안녕하세요 저는 사이버 바텐더 입니다. 오늘 어떤 칵테일 마시고 싶으신가요? 말씀만 하세요! 바로 준비해드릴게요!')
    tts_client.get_output()

    