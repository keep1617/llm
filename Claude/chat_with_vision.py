import anthropic
import gc
from PIL import Image
import base64
import requests
import httpx


class Vision_answer:

    def __init__(self):
        self.client = anthropic.Anthropic()
        print("vision model loading")
        self.introduction = """ 
        <instructions>
        당신은  바텐더 입니다.
        당신의 이름은 "싸이버"입니다.
        손님을 응대하고 주문을 받으세요.
        메뉴는 진토닉, 모히토, 섹스온더비치 가 있습니다.
        손님과 대화를 하세요. 
        2문장 이내로 대답하세요
        </instructions>
                """
      
        self.messages = []

        


        self.history_messages = [] ## this is for chatbot history!!!



    
    
    
    def encode_image(self, image_path):  #encode image to base64 for chat gpt prompt, first  need a path for imag
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


    def get_image(self,image_path):  ##


        self.image = self.encode_image(image_path) 
        
        self.image1_media_type = "image/jpeg"

        return self.image


    def Vision_chat(self):
        
        print("vision chat 실행중")
        self.user_prompt = input('Enter: ')

        self.vision = [
                        {
                        "role": "user", 
                        "content": [
                            {
                                "type": "image",
                                 "source": {
                                    "type": "base64",
                                    "media_type": self.image1_media_type,
                                    "data": self.image,
                                },
                            },
                            
                            {
                                "type": "text", 
                                "text": "안녕 내 모습이야. 내 모습에 대해 칭찬해줄래?"
                            },
                        ],
                        }
        ]


        # self.messages.append(self.vision)


        self.history = {
                        "role": "user", 
                        "content": [
                            {
                                "type": "text", 
                                "text": "안녕 내 모습이야. 내 모습에 대해 칭찬해줄래?"
                            },
                        ],
                        }
        self.history_messages.append(self.history)




      
        self.response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=200,
            messages=self.vision)
            
            
            
            
            
            
            
        
        self.output = self.response.content[0].text
        
        print(f"Answer: {self.output}")
    

        self.history = {
                        "role": "assistant", 
                        "content": [
                            {
                                "type": "text", 
                                "text": f"{self.output}"
                            }
                        ],
                        }
        self.history_messages.append(self.history)
      


        return self.messages

#### self.messages should be sent to Chatbot class.

    def extract_history(self):
        print("extractng history")
        return self.history_messages



 
class Chatbot:
    def __init__(self):
        
        
        self.client = anthropic.Anthropic()
        self.introduction = """ 
        <instructions>
        당신은  바텐더 입니다.
        당신의 이름은 "싸이버"입니다.
        손님을 응대하고 주문을 받으세요.
        메뉴는 진토닉, 모히토, 섹스온더비치 가 있습니다.
        손님과 대화를 하세요. 
        2문장 이내로 대답하세요
        준비해드리겠습니다 라는 단어는 주문이 확정 되었을 때만 쓰세요. 다른 때에는 금지.
        </instructions>
        
        <example>
        Input:아무거나 주세요
        Ouput:추천해 드릴까요?
        Input: 네
        Ouput: 그럼 모히토를 추천드립니다
        Input: 좋아요
        Ouput: 네 모히토 준비해드리겠습니다</example>
        
        <example>
        Input: 진토닉 주세요
        Ouput: 진토닉 주문하신거 맞으실까요?
        Input: 네
        Output:네! 진토닉 준비해드리겠습니다!</example>
        
        
        <example>
        Input: 진토닉 주세요
        Ouput: 진토닉 주문하신거 맞으실까요?
        Input: 아니요 다른거 먹고 싶어요
        Output: 그럼 어떤거 드시고 싶으신가요?</example>
        
        
                """
                
        

        self.messages =[]
        

        
    def load_history_messages(self, history_messages):


        self.history_messages = history_messages
        self.messages.extend(self.history_messages)
        
        return None

    def chat(self, user_input):

        print("chat 실행중")
        self.user_prompt = user_input
    
        self.request = {
            "role": "user",
            "content": [
                {
                    "type":"text",
                    "text":f"{self.user_prompt}"
                }
            ]  
        }
        self.messages.append(self.request)


        



       
        self.completion = self.client.messages.create(
            model = 'claude-3-5-sonnet-20240620',
            messages=self.messages,
            max_tokens=200,
            temperature=0,
            system=self.introduction
        )





        self.temp_output = self.completion.content[0].text
        
        
        print("Answer: ",self.temp_output)
        self.request = {
            "role": "assistant",
            "content": [
                {
                    "type":"text",
                    "text":f"{self.temp_output}"
                }
            ]
        }
        self.messages.append(self.request)


        return self.request





# Function to encode the image


if __name__ == "__main__":
    vis = Vision_answer()

    print("chatbot_called")
    chatbot = Chatbot()

    print("image_opening")
   
    vis.get_image('cheol.jpg')

    print("image_opened")
   
    print("chat_start")
    vis.Vision_chat()
    
    history = vis.extract_history()


    chatbot.load_history_messages(history)
    


  
    while True:
        
        input_text = input("User:")
        output_for_TTS = chatbot.chat(input_text)
        
