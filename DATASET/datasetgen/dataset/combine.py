import json

json_file_path = ['choice_dataset.json', 'recommend_dataset.json']
combined_data=[]

for file_path in json_file_path:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        combined_data.extend(data)
        
        
with open("combined_output.json", 'w', encoding='utf-8') as ouput_file:
    json.dump(combined_data, ouput_file, ensure_ascii=False, indent=4)
    
    
print("2개의 JSON 파일이 하나로 결합되었습니다!")