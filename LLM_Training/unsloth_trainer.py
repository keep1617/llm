from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments, TextStreamer
from unsloth import is_bfloat16_supported
import torch


max_seq_length = 2048
dtype = None
load_in_4bit = True

fourmit_models = [
"unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"
]

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Meta-Llama-3.1-8B",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    token = "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"
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # 0보다 큰 숫자를 선택하세요! 권장값: 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj","embed_tokens", "lm_head",],
    lora_alpha = 16,
    lora_dropout = 0, # 어떤 값이든 지원하지만, 0이 최적화되어 있습니다
    bias = "none",    # 어떤 값이든 지원하지만, "none"이 최적화되어 있습니다
    # [새로운 기능] "unsloth"는 30% 더 적은 VRAM을 사용하며, 2배 더 큰 배치 크기를 지원합니다!
    use_gradient_checkpointing = "unsloth", # 매우 긴 컨텍스트의 경우 True 또는 "unsloth" 사용
    random_state = 3407,
    use_rslora = False,  # 순위 안정화 LoRA를 지원합니다
    loftq_config = None, # 그리고 LoftQ도 지원합니다
)




from datasets import load_dataset
# 한국어 데이터셋 로드
dataset = load_dataset("adfa5456/hi", split = "train")
# 데이터셋에 프롬프트 포맷팅 함수 적용
# dataset = dataset.map(formatting_prompts_func, batched = True,)



trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, # 짧은 시퀀스의 경우 학습 속도를 5배 빠르게 할 수 있습니다.
    args = TrainingArguments(
        per_device_train_batch_size = 2, # 각 장치별 배치 크기를 2로 설정합니다.
        gradient_accumulation_steps = 4, # 그래디언트 누적 단계를 4로 설정합니다.
        warmup_steps = 5, # 워밍업 단계를 5로 설정합니다.
        num_train_epochs = 1, # 전체 학습을 위해 이 값을 1로 설정합니다.
        max_steps = -1, # 최대 단계를 60으로 설정합니다.
        learning_rate = 2e-4, # 학습률을 2e-4로 설정합니다.
        fp16 = not is_bfloat16_supported(), # bfloat16 지원 여부에 따라 fp16을 설정합니다.
        bf16 = is_bfloat16_supported(), # bfloat16 지원 여부에 따라 bf16을 설정합니다.
        logging_steps = 1, # 로그 기록 단계를 1로 설정합니다.
        optim = "adamw_8bit", # 옵티마이저를 adamw_8bit로 설정합니다.
        weight_decay = 0.01, # 가중치 감소를 0.01로 설정합니다.
        lr_scheduler_type = "linear", # 학습률 스케줄러 유형을 linear로 설정합니다.
        seed = 3407, # 시드를 3407로 설정합니다.
        output_dir = "outputs", # 출력 디렉토리를 "outputs"로 설정합니다.
    ),
)


trainer_stats = trainer.train()

# model.push_to_hub("adfa5456/llama3-1_0922", token = "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") # 허깅페이스에 저장하기
# tokenizer.push_to_hub("adfa5456/llama3-1_0922", token = "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") # 허깅페이스에 저장하기

model.save_pretrained("temp_model")
tokenizer.save_pretrained("temp_model")



# inference



