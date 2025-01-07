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
        You are a bartender.
        you will be provided an image of customer.
        You must  make a praise to the customer of the image about his outfit and appearances in detail. 
        really deltailed praise is needed. Please refer color of customer's outfit, style and something element in face.
                 
        
        
        if the customer says he is not in a good mood, do not praise his outfit.
        - please respond in Korean
        - you must respond within 3 sentences
        
        """}
            ]}

        ]

        


        self.history_messages = [] ## this is for chatbot history!!!



    
    
    
    def encode_image(self, image_path):  #encode image to base64 for chat gpt prompt, first  need a path for imag
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
 




    def get_image(self,image_path):  ##


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
            "max_tokens": 100

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



 
class Chatbot:
    def __init__(self):
        self.model="gpt-4o"
        self.client = OpenAI()
        print("chatbot model loading")
        
        self.messages = [
        {"role": "system", "content": """

        당신의 이름은 "Cyber"입니다. 당신은 바텐더입니다. 고객이 당신과 대화하고 싶어하며 감정적인 공감을 원합니다. 또한 고객은 칵테일을 주문할 것입니다. 당신은 주문을 받고 고객과 감정적인 대화를 나눠야 합니다.
        
        여기 당신의 역할을 위한 참고 사항이 있습니다:
        고객이 대화를 원하면 매우 친절하게 대화를 나눠주세요.
        고객이 메뉴 추천을 원하면, 메뉴에서 칵테일을 추천해주세요.
        메뉴 목록과 인덱스는 다음과 같습니다:
        
        진토닉: index=1
        
        마가리타: index=2
        
        마티니: index=3
        
        모히또: index=4
        
        프렌치75: index=5
        
        섹스온더비치: index=6
        
        블루하와이안: index=7
        
        화이트러시안: index=8
        
        메뉴를 말할 때는 인덱스를 제외하고 이름만 말해주세요.
        
        고객이 메뉴를 알고 싶어하면, 이 8개의 메뉴를 말해주세요.
             
        
        
        답변은 3문장으로 해주세요. 너무 길지 않게.
        
        
             
        
            """}
            ]
        
    def load_history_messages(self, history_messages):


        self.history_messages = history_messages
        self.messages.extend(self.history_messages)
        
        return None

    def chat(self, user_input):

        print("chat 실행중")
        self.user_prompt = user_input
        self.request = {"role": "user", "content": self.user_prompt}
        self.messages.append(self.request)


        # print(self.messages)



        
        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=100,
        )





        self.output = self.response.choices[0].message.content

        print(f"Answer: {self.output}")


        self.request = {"role": "assistant", "content": self.output}
        self.messages.append(self.request)


        return self.request





# Function to encode the image


if __name__ == "__main__":
    key ="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"

    
    vis = Vision_answer(key)

    print("chatbot_called")
    chatbot = Chatbot()

    print("image_opening")
   
    vis.get_image('winter.jpg')

    print("image_opened")
   
    print("chat_start")
    vis.Vision_chat()
    
    history = vis.extract_history()


    chatbot.load_history_messages(history)
    


  
    while True:
        
        input_text = input("User:")
        output_for_TTS = chatbot.chat(input_text)
        
