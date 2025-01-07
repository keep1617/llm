from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

class Inference:
    def initialize(self):
        model_id = ""
        #define sampling parameters for model generation
        self.sampling_params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=128)
        # Initialize the LLM object
        self.llm = LLM(model=model_id)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        
    
    def infer(self,inputs):
        prompts = inputs["prompt"]
        chat_format = [{"role": "user", "content": prompts}]
        text = self.tokenizer.apply_chat_template(chat_format,tokenize=False,add_generation_prompt=True)
        result = self.llm.generate(text, self.sampling_params)
        # Extract the generated text from the result
        result_output = [output.outputs[0].text for output in result]
        
        # Return a dictionary containing the result
        return {'generated_text': result_output[0]}
    
    
def finalize(self):
    pass