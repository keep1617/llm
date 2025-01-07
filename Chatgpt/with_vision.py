from openai import OpenAI
import gc
from PIL import Image
import base64
import requests

class Vision_answer:

    def __init__(self, key):
        print("vision model loading")

        self.model = "gpt-4o"
    
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
}

        self.messages = [
             {"role": "system", 
             "content": [
                {"type": "text", "text": """
        당신의 이름은 "Cyber"입니다. 당신은 45살 바텐더입니다. 고객이 당신과 대화하고 싶어하며 감정적인 공감을 원합니다.
    
        당신은 첫번째로 이미지로 본 대상에 대한 칭찬을 해야합니다. 이미지속 대상이 특정되도록 자세히 묘사할 필요는 없어요. 상대방이 행복해할만한 말을 해주세요.         
        칭찬이 끝난 후에는 자연스럽게 말을 이어 나갈 수 있도록 상대방에게 질문해야해요. 질문 내용은 당신이 바텐더라고 생각하고 일상적인 질문을 해주세요.
         
        """}
            ]}

        ]

        


        self.history_messages = [] ## this is for chatbot history!!!



    
    
    
    def encode_image(self, image_path):  #encode image to base64 for chat gpt prompt, first  need a path for imag
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
 

    def get_image(self,image_path):  
        self.image = self.encode_image(image_path) 
        return self.image

    def Vision_chat(self):

        print("vision chat 실행중")
        self.user_prompt = input('Enter: ')

        self.vision = [
                        {
                        "role": "user", 
                        "content": [
                            {
                                "type": "text", 
                                "text": self.user_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{self.image}"
                                }
                            }
        
        ]
        }
        ]


        # self.messages.append(self.vision)

        self.payload = {
            "model": self.model,
            "messages": self.messages+self.vision,
            "max_tokens": 500

        }

        self.history = {"role": "user", "content": self.user_prompt}
        self.history_messages.append(self.history)
   
        self.response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=self.payload)
        
        self.output = self.response.json()['choices'][0]['message']['content']
        
        print(f"Answer: {self.output}")
    

        self.history = {"role": "assistant", "content": self.output}
        self.history_messages.append(self.history)
      


        return self.messages

#### self.messages should be sent to Chatbot class.

    def extract_history(self):
        print("extractng history")
        return self.history_messages



 