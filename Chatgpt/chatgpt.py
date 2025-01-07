from openai import OpenAI
import random


class Chatbot:

    def __init__(self):
        
        self.client = OpenAI()
        self.introduction = """ 
                당신의 이름은 "Cyber"입니다. 당신은 바텐더입니다. 고객이 당신과 대화하고 싶어하며 감정적인 공감을 원합니다. 또한 고객은 칵테일을 주문할 것입니다. 당신은 주문을 받고 고객과 감정적인 대화를 나눠야 합니다.
        
        여기 당신의 역할을 위한 참고 사항이 있습니다:
        고객이 대화를 원하면 매우 친절하게 대화를 나눠주세요.
        고객이 메뉴 추천을 원하면, 메뉴에서 칵테일을 추천해주세요.
        메뉴 목록과 인덱스는 다음과 같습니다:
        진토닉, 마가리타, 마티니, 모히또, 프렌치75, 섹스온더비치
        메뉴를 말할 때는 인덱스를 제외하고 이름만 말해주세요.
        
       고객이 추천을 원하는 것 같으면 "추천해줘 라고 말해주세요" 라고 말해.
       
       고객이 주문을 하면  저 6가지 메뉴 중에서 고객이 주문한 메뉴를 언급하고, "준비해 드리겠습니다!"라고 해
        
        답변은 3문장으로 해주세요. 너무 길지 않게.

                """

        self.messages =[
            {
                "role": "system",
                "content": f"{self.introduction}"
            }
        ]


        
        
    def chat(self, input):
        self.temp_input = input
        self.input = {
            "role": "user",
            "content": f"{self.temp_input}"
        }
        self.messages.append(self.input)
        # input history 추가
        
        self.completion = self.client.chat.completions.create(
            model = 'gpt-4o',
            messages=self.messages,
            max_tokens=100
        )
        self.temp_output = self.completion.choices[0].message.content
        
        
        
        self.output = {
            "role": "assistant",
            "content": f"{self.temp_output}"
        }
        
        self.messages.append(self.output)  #ouput history 추가-
        
      
        print(self.temp_output)
        
        return None

    def append_intro(self, customer_emo):
        self.customer_emo = customer_emo
        self.introduction = "".join([self.customer_emo,self.introduction])
        print(self.introduction)
        return None



class emotion_check:

    def __init__(self):
        self.customer_emotion = ""
        self.emotion = ""
        self.choice= ["sad", "happy"]
        pass
    
    def feeling(self, emotion):
        self.emotion = emotion
        if self.emotion == "sad" : 
            self.customer_emotion = """- customer looks sad"""
        elif self.emotion == "happy":
            self.customer_emotion = """- customer looks happy"""
        
        return self.customer_emotion
    

    def generate(self):
        self.selected_choice = random.choice(self.choice)

        return self.selected_choice









if __name__== "__main__":
    _ = Chatbot()
    emo = emotion_check()
    emotion = emo.generate()
    print(emotion)
   
    custom_emotion = emo.feeling(emotion)
    
    _.append_intro(custom_emotion)
    
    while True:
        
        input_text= input("USER input: " )
        if input_text=="끝":
            break
            
        _.chat(input_text)
    

        
    