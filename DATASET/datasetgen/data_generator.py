import random
import json
import yaml
import itertools
import re


def replace_dataset(row, grammer,keys, values):
    data = []
    gen_data = []
    # i = 0
    data.clear()
    for combination in itertools.product(*values): 
        
        # print(f"combination is {combination}")
        ## 모든 key에 대한 value의 조합이 생성됨-1turn 돌 때마다
        replace_dict = dict(zip(keys, combination))
        
            ##key랑 combination이 짝찌어져 있는 상태   
        
        
        for element in row:
            
            
            if 'content' in element:
                    # 플레이스홀더를 현재 key와 value로 대체
                # print(f"for replace: {replace_dict}")
                
                new_content = element['content'].format(**replace_dict)
                new_element = element.copy()
                new_element['content'] = new_content
                
                data.append(new_element)
        #         print(new_element)
        # gen_data.append(data)
        # i = i+1
    
    # print(f"iteration is :{i}")
    
    
            
    return data




def extract_keys(row):
    
    extracted_keys = []
    pattern = r'\{([\w가-힣]+)\}'
    

    for element in row:
        if 'content' in element:
            hi = re.findall(pattern, element['content'])
            
        extracted_keys.extend(hi)  # 추출된 키를 리스트에 추가
            
            
    unique_keys = list(set(extracted_keys))
    
    return unique_keys

def extract_values(keys, grammer):
    keys = keys
    values = []
    for item in keys:
        values.append(grammer[item])
    # print(values)
    return values


def unpack_list(list):
    unpacked_list = []
    packed_list = list
    for sublist in packed_list:
        for item in sublist:
            unpacked_list.append(item)
   
    return unpacked_list


def after_process(dataset):
    
    part_dataset = []
    after_dataset = [] 
    i = 0
    for item in dataset:
        
        
        
        if item["role"] == "system" and i!=0:
            after_dataset.append(part_dataset.copy())
            
            part_dataset.clear()
            
            
        part_dataset.append(item)
       
        i = i+1
        
    
    # print(after_dataset)
    
    return after_dataset

# 추출된 키: ['우울문장mid', '좋은감정mid', '추천멘트', '기분좋은메뉴', '우울반응', '우울메뉴', '기분좋은반응']


if __name__ == "__main__":
    with open('recommend.json', 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    
    # print(type(dataset))    
    with open('grammer.yaml', 'r', encoding='utf-8') as file:
        grammer = yaml.safe_load(file)
        
    generated_data = []
    
    dataset_data = []
    
    after_processed_dataset = []
    for row in dataset:
        
        row_keys = extract_keys(row)

        row_values = extract_values(row_keys, grammer)
        
        generated_data.append(replace_dataset(row, grammer, row_keys, row_values))
        
        dataset_data = unpack_list(generated_data)
        
        
    after_processed_dataset = after_process(dataset_data)
    
        
    print(f"length of this is : {len(after_processed_dataset)}")
        
   
       




    with open('recommend_dataset.json', 'w', encoding='utf-8') as file:
            json.dump(after_processed_dataset, file, ensure_ascii=False, indent=4)






    print("데이터셋이 recommend_dataset.json 파일로 저장되었습니다.")



