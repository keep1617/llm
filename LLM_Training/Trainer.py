import os
import torch, gc
from datasets import load_dataset

from transformers import(

    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)

from peft import LoraConfig
from trl import SFTTrainer

import huggingface_hub
huggingface_hub.login('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')


base_model = "MLP-KTLim/llama-3-Korean-Bllossom-8B"

dataset = "adfa5456/hi"

new_mode = "Llama3-bartender"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if device=="cuda": torch.cuda.empty_cache()



if torch.cuda.get_device_capability()[0] >= 8:
    attn_implementation = "flash_attention_2"
    torch_dtype = torch.bfloat16

else:
    attn_implementation="eager"
    torch_dtype = torch.float16



 ## QLoRA config

quant_config = BitsAndBytesConfig(

     load_in_4bit=True,
     bnb_4bit_compute_dtype=torch_dtype,
     bnb_4bit_quant_type="nf4",
     bnb_4bit_use_double_quant=False,
 )

dataset = load_dataset(dataset, split="train")







model = AutoModelForCausalLM.from_pretrained(
     base_model,
     quantization_config = quant_config,
     device_map={"": 0}


 )

model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(
    base_model,
    trust_remote_code = True)

tokenizer.pad_token = tokenizer.eos_token
tokenizer.paddding_side = "right"


peft_params = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r = 64,
    bias = "none",
    task_type="CASUAL_LM",
)


training_params = TrainingArguments(
    output_dir="./results",
    num_train_epochs=10,
    per_device_eval_batch_size=2
    gradient_accumulation_steps=1,
    optim="paged_adamw_32bit",
    save_steps=25,
    logging_steps=25,
    learning_rate=2e-4,
    weight_decay=0.001,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="constant",
    report_to="tensorboard"


)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_params,
    dataset_text_field="text",
    max_seq_length=None,
    tokenizer=tokenizer,
    args=training_params,
    packing=False,

)
trainer.train()


logging.set_verbosity(logging.CRITICAL)



prompt = "안녕하세요 오늘 기분이 아주 좋아요"
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
result = pipe(f"<s>[INST] {prompt} [/INST]")
print(result[0]['generated_text'])


model.push_to_hub("adfa5456/bartender_mode0921")
tokenizer.push_to_hub("adfa5456/bartender_mode0921")