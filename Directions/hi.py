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


base_model = "beomi/Llama-3-Open-Ko-8B"

dataset = "adfa5456/convdataset"

new_mode = "Llama3-bartender"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if device=="cuda": torch.cuda.empty_cache()

torch.cuda.memory_allocated()
torch.cuda.max_memory_allocated()
torch.cuda.memory_reserved()
torch.cuda.max_memory_reserved()


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




print(dataset)


model = AutoModelForCausalLM.from_pretrained(
     base_model,
     quantization_config = quant_config,
     device_map={"": 0}


 )

model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
# Must add EOS_TOKEN at response last line
tokenizer.pad_token = tokenizer.eos_token
# ★수정 포인트!!! 기존 # tokenizer.padding_side = "right"
EOS_TOKEN = tokenizer.eos_token
def prompt_eos(sample):
    sample['conversation'] = sample['conversation']+EOS_TOKEN
    return sample
datasethk = dataset.map(prompt_eos)

print(dataset[0])

peft_params = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r = 64,
    bias = "none",
    task_type="CASUAL_LM",
)


training_params = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_eval_batch_size=1,
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
    train_dataset=datasethk,
    peft_config=peft_params,
    dataset_text_field="conversation",
    max_seq_length=None,
    tokenizer=tokenizer,
    args=training_params,
    packing=False,

)
trainer.train()


logging.set_verbosity(logging.CRITICAL)

prompt = "오늘 기분 좋다"
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
result = pipe(f"<s>[INST] {prompt} [/INST]")
print(result[0]['generated_text'])
