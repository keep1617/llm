import itertools

# 예시 데이터와 임베딩 대체 값
dataset = [
    {
        "role": "user",
        "content": "오늘 기분이 {우울문장mid}, 뭐가 좋을까요?"
    },
    {
        "role": "assistant",
        "content": "{우울반응}, 고객님의 기분을 위해 {우울메뉴} {추천멘트}"
    }
]

# 키와 임베딩 대체 값
keys = ['우울문장mid', '우울반응', '우울메뉴', '추천멘트']
values = [
    ['우울해요', '안 좋아요'],
    ['괜찮으시길 바랍니다', '조금 더 노력해보세요'],
    ['진토닉', '마가리타'],
    ['추천드립니다', '한 번 시도해보세요']
]

# 모든 조합을 생성
for combination in itertools.product(*values):
    # 매 조합마다 dataset을 복사하여 처리
    sentence = [dict(item) for item in dataset]  # dataset의 딥 복사

    # 각 key와 value 쌍을 순회
    for key, value in zip(keys, combination):
        for row in sentence:
            if 'content' in row:
                # 플레이스홀더를 현재 key와 value로 대체
                row['content'] = row['content'].replace(f'{{{key}}}', value)

    # 결과 출력
    for item in sentence:
        print(item['content'])
