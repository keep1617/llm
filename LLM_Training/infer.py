from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import torch

model_id = "beomi/Llama-3-Open-Ko-8B-Instruct-preview"



def chat(instuction, input_text=""):
    prompt = """
    
    {"role": "system", "content": "{0}"},
    {"role": "user", "content": "{1}"},
    {"role": "assistant", "content": "{2}"},
"""

    tokenizer = AutoTokenizer.from_pretrained(model_id)



    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype="auto",
        device_map="auto",
    )


    inputs = tokenizer.apply_chat_template(
        prompt.format(
            instruction,
            input_text,
            "",
            ),
        add_generation_prompt=True,
        return_tensors="pt"
    ).to("cuda")

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
    inputs,
    max_new_tokens=512,
    eos_token_id=terminators,
    do_sample=True,
    temperature=1,
    top_p=0.9,
    )
    
    text_streamer = TextStreamer(tokenizer)
    
    with torch.no_grad():
        _ = model.generate(**inputs, streamer=text_streamer, max_new_tokens=1024)
    
    
    

print("채팅을 시작합니다. 종료하려면 'quit'를 입력하세요.")
while True:
    instruction = "너의 이름은 바텐더 싸이버야. 너의 목표는 고객의 질문에 잘 대답하고 주문을 받아야해. 너는 칵테일 바텐더야. 너가 할 일은 고객과 대화하기, 고객의 기분에 맞춰서 음료 추천하기, 주문 받기야.메뉴는 진토닉,마가리타, 마티니, 모히토, 프렌치 75, 섹스온더비치, 블루하와이언, 화이트 러시안이 있어. 만약 메뉴에 없는 걸 주문하면 없다고 해."
    input_text = input("추가 입력: ")
    if input_text.lower() == 'quit':
        break
    print("\nAI 응답:")
    chat(instruction, input_text)
    print("\n")
    
print("채팅을 종료합니다.")