import os, sys
import torch
import numpy as np


from Cheol import LLM_BASE_MODEL, MAX_TOKEN_LENGTH, ROS_LLM_INPUT_TOPIC, ROS_LLM_OUTPUT_TOPIC, ROS_LLM_DONE_TOKEN, format_prompt



from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TextStreamer,
    pipeline,
    logging,
)
from peft import LoraConfig
from trl import SFTTrainer

import rospy
from rospy import Publisher
from std_msgs.msg import String



class LLMChat:
    def __init__(self):
        
        self.device = "cuda:0"
        self.model = None
        self.tokenizer= None
        self.streamer = None
        self.llm_stream_response = None
        self.llm_stream_text = None
        

        
    def load_model(self):
        base_model = AutoModelForCausalLM.from_pretrained(LLM_BASE_MODEL, device_map = self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(LLM_BASE_MODEL, device_map = self.device)
        self.model = AutoModelForCausalLM.from_pretrained(LLM_BASE_MODEL, device_map = self.device)
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True)
    

        
    def chat(self, prompt):
        
        full_prompt = format_prompt(prompt)
        
        
        
        
        
        
        self.pipeline = self.transformers.pipeline(
            "text-generation",
            model = self.model,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map = self.device
        )
        terminators = [
        self.tokenizer.eos_token_id,
        self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
    
        
        
        outputs = self.pipeline(
            full_prompt,
            max_new_tokens=MAX_TOKEN_LENGTH,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p = 0.9,
        )
        
        text = outputs[0]["generated_text"][-1]
        
        return text
    
    
    #     def init_sub(self):
    
    
    
    
#     def prompt_callback(msg):
        
    
    
#     def init_pub(self):
        
    
    
#     def preprocess(self,prompt):
        
        
if __name__ == "__main__":
    _ = LLMChat()
    _.load_model()
    while True:
        output = _.chat(input("user: "))
        print(output)    
    