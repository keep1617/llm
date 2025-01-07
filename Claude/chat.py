import anthropic

import random


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
        


        
        
    def chat(self, input):
        self.temp_input = input
        self.input = {
            "role": "user",
            "content": [
                {
                    "type":"text",
                    "text":f"{self.temp_input}"
                }
            ]  
        }
        self.messages.append(self.input)
        # input history 추가
        
        self.completion = self.client.messages.create(
            model = 'claude-3-5-sonnet-20240620',
            messages=self.messages,
            max_tokens=200,
            temperature=0,
            system=self.introduction
        )
        self.temp_output = self.completion.content[0].text
        
        
        
        self.output = {
            "role": "assistant",
            "content": [
                {
                    "type":"text",
                    "text":f"{self.temp_output}"
                }
            ]
        }
        
        self.messages.append(self.output)  #ouput history 추가-
        
      
        print(self.temp_output)
        
        return None







if __name__== "__main__":
    _ = Chatbot()
    
    while True:
        
        input_text= input("USER input: " )
        if input_text=="끝":
            break
            
        _.chat(input_text)
    

        
    
