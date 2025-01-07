import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
MDLS_DIR = os.path.join(ROOT_DIR, 'Modules')
ROS_VERSION = 1 
HUGGINGFACE_TOKEN = "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"




# --------------------LLM SETTINGS -------------------------------------


LLM_BASE_MODEL = "beomi/Llama-3-Open-Ko-8B"
PEFT_MODEL = "adfa5456/bartender2_0830"
MAX_TOKEN_LENGTH = 200
ROS_LLM_INPUT_TOPIC = '/llm_input'
ROS_LLM_OUTPUT_TOPIC = '/LLM_output'
ROS_LLM_DONE_TOKEN = '<|eot_id|>:'


# --------------------- STT SETTINGS ----------------------
ROS_START_STT_TOPIC = '/stt_start'
ROS_STT_RESULT_TOPIC = '/voice_input'




# --------------------- GOOGLE TTS SETTINGS -------------





system_prompt = """
너의 이름은 바텐더 싸이버야. 너는 제우스 대회를 참가 하고 있어. 너의 목표는 고객의 질문에 잘 대답하고 주문을 받아야해.
너는 칵테일 바텐더야.
너가 할 일은 고객과 대화하기, 고객의 기분에 맞춰서 음료 추천하기, 주문 받기야.
메뉴는 마티니,핑크 레이디,섹스온더비치,블루사파이어,허니문,올림픽이 있어.
"""


def format_prompt(prompt):
    text = f"""
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}<|eot_id|>
    <|start_header_id|>user<|end_header_id|>{prompt}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """
    
    
     
    #    text = f"""
    # {"role" : "system", "content" : {system_prompt}},
    # {"role" : "user", "content" : {prompt}},
    # """
    
    
    return text

import sys
import signal

def cleanup_before_exit(signum, frame):
    print("\nTerminating the script...")
    sys.exit(0)

signal.signal(signal.SIGTSTP, cleanup_before_exit)
    









# print(f'__file__: {MDLS_DIR}')