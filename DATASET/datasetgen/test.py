
import re


def extract_keys(text):
    pattern = r'\{([\w가-힣]+)\}'
    keys = re.findall(pattern,text)
    
    unique_keys = list(set(keys))
    
    return unique_keys




text = example_text = "오늘 기분이 {우울문장mid}, {우울반응} 뭐가 좋을까요? 그리고 {우울반응}과 {우울메뉴} {추천멘트}도 있습니다."

extracted_keys = extract_keys(text)

print(f"추출된 키: {extracted_keys}")