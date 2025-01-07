from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments, TextStreamer

import torch


import unsloth
from transformers import TextStreamer
import torch

global model
global tokenizer

def chat(instruction, input_text=""):


    



   
    alpaca_prompt = """
    ### Instruction:
    {0}

    ### Input:
    {1}

    ### Response:
    {2}"""

    inputs = tokenizer(
        [
            alpaca_prompt.format(
                instruction,  # instruction
                input_text,   # input
                "",           # output - leave this blank for generation!
            )
        ],
        return_tensors="pt"
    ).to("cuda")


    
    FastLanguageModel.for_inference(model) # Enable native 2x faster inference
    text_streamer = TextStreamer(tokenizer)
    with torch.no_grad():
        _ = model.generate(**inputs, streamer=text_streamer, max_new_tokens=1024)




# inference





print("채팅을 시작합니다. 종료하려면 'quit'를 입력하세요.")

model, tokenizer = FastLanguageModel.from_pretrained(
    
    model_name = "./temp_model", # YOUR MODEL YOU USED FOR TRAINING
    max_seq_length = 1024,
    dtype = None,
    load_in_4bit = True,
)

while True:
    instruction = "너의 이름은 바텐더. 너의 목표는 고객의 질문에 잘 대답하고 주문을 받아야해. 너는 칵테일 바텐더야. 너가 할 일은 고객과 대화하기, 고객의 기분에 맞춰서 음료 추천하기, 주문 받기야.메뉴는 진토닉,마가리타, 마티니, 모히토, 프렌치 75, 섹스온더비치, 블루하와이언, 화이트 러시안이 있어. 만약 메뉴에 없는 걸 주문하면 없다고 해."
    
    input_text = input("추가 입력(없으면 Enter): ")
    if input_text.lower() == 'quit':
        break
    print("\nAI 응답:")
    chat(instruction, input_text)
    print("\n")

print("채팅을 종료합니다.")