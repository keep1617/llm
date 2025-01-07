
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments, TextStreamer

import torch
from datasets import load_dataset


from peft import LoraConfig
from trl import SFTTrainer
import pandas as pd

# from google.colab import drive
# drive.mount("/content/gdrive")

import huggingface_hub

token = "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"
huggingface_hub.login(token)
# # set base model path
# # base_model = "beomi/Llama-3-Open-Ko-8B"
# base_model = "meta-llama/Meta-Llama-3-8B-Instruct"
# # set new model path
# new_model = "Llama3-hkcode-Ko-8b-youtube-meta"

# dataset_namehk = "hyokwan/localllama"
dataset_namehk = "adfa5456/hee0923"
datasethk = load_dataset(dataset_namehk, split="train")


model, tokenizer = FastLanguageModel.from_pretrained(
    
    model_name = "./temp_model", # YOUR MODEL YOU USED FOR TRAINING
    max_seq_length = 1024,
    dtype = None,
    load_in_4bit = True,
)
EOS_TOKEN = tokenizer.eos_token

def create_text_column(example):
    # 'text' 컬럼 생성


    instruction = example['0']['content'] + EOS_TOKEN
    input = example['1']['content'] + EOS_TOKEN
    output = example['2']['content'] + EOS_TOKEN
    text = f""""

    ### Instruction:
    {instruction}

    ### Input:
    {input}

    ### Response:
    {output}"""

    example["text"] = text 
    return example







# def create_instruction_column(example):
#     # 'instruction' 컬럼 생성
#     instruction = f"너의 이름은 바텐더 싸이버야. 너의 목표는 고객의 질문에 잘 대답하고 주문을 받아야해. 너는 칵테일 바텐더야. 너가 할 일은 고객과 대화하기, 고객의 기분에 맞춰서 음료 추천하기, 주문 받기야.메뉴는 진토닉,마가리타, 마티니, 모히토, 프렌치 75, 섹스온더비치, 블루하와이언, 화이트 러시안이 있어. 만약 메뉴에 없는 걸 주문하면 없다고 해."
#     example["instruction"] = instruction
#     return example

# # 'instruction' 컬럼 생성
# datasethk = datasethk.map(create_instruction_column)

# 'text' 컬럼 생성
datasethk = datasethk.map(create_text_column)

i = 0
# def text_conversation_append(example):
#
#     for index, row in df.iterrows():
df = pd.DataFrame(datasethk)
dataset = datasethk.from_pandas(df)
dataset.push_to_hub("adfa5456/hi")







# conv_string = []
# temp_string = []

# for row in df.itertuples():
#     my_string = ''.join(temp_string)

#     conv_string.append(my_string)
#     temp_string.clear()
#     temp_string.append(row.text)

# print(conv_string[0])

# with open('real_humanbot_dataset.csv', 'w', newline = '', encoding='utf-8') as csvfile:
#     fieldnames=['text']
#     writer= csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()

#     for text in datasethk:
#         writer.writerow({'text': text})

# df = pd.read_csv('real_humanbot_dataset.csv')
# print(datasethk[0])

