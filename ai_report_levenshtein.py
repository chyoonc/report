import pandas as pd

# 레벤슈타인 거리 함수
def calc_distance(a, b):
    ''' 레벤슈타인 거리 계산하기 '''
    if a == b: return 0  # 같으면 0을 반환
    a_len = len(a)  # a 길이
    b_len = len(b)  # b 길이
    if a == "": return b_len
    if b == "": return a_len
    
    matrix = [[] for i in range(a_len+1)]  # 리스트 컴프리헨션을 사용하여 1차원 초기화
    for i in range(a_len+1):  # 0으로 초기화
        matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
    # 0일 때 초깃값을 설정
    for i in range(a_len+1):
        matrix[i][0] = i
    for j in range(b_len+1):
        matrix[0][j] = j
    # 표 채우기
    for i in range(1, a_len+1):
        ac = a[i-1]
        for j in range(1, b_len+1):
            bc = b[j-1] 
            cost = 0 if (ac == bc) else 1  # 파이썬 조건 표현식 예:) result = value1 if condition else value2
            matrix[i][j] = min([
                matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
            ])
    return matrix[a_len][b_len]

# 챗봇 클래스를 정의
class SimpleChatBot:
    # 객체 초기 설정(생성자 설정)
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)  # 데이터 파일로부터 질문과 답변을 로드

    # CSV파일에서 데이터를 읽는 메서드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)  # CSV 파일을 읽어옴
        questions = data['Q'].tolist()   # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()  # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers  # 질문과 답변 리스트를 반환

    # 레벤슈타인 거리 기반 답변 메서드
    def levenshtein_Distance_answer(self, input_sentence):
        # print("levenshtein_Distance_answer 호출")
        distances = []  # 레벤슈타인 거리를 저장할 리스트를 초기화
        for question in self.questions:  # 모든 질문을 순회
            dist = calc_distance(input_sentence, question)  # 입력 문장과 학습데이터 질문 간의 레벤슈타인 거리를 계산
            distances.append(dist)  # 계산된 거리를 리스트에 추가
        best_match_index = distances.index(min(distances))  # 가장 작은 레벤슈타인 거리의 학습데이터 질문의 인덱스를 찾음
        # print(f"유저 질문: {input_sentence}\n선택된 질문: {self.questions[best_match_index]}\ncsv 번호: {best_match_index+2}\n거리 값: {min(distances)}\n")
        return self.answers[best_match_index]  # 가장 유사한 학습데이터 질문에 해당하는 답변을 반환

# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')  # 사용자 입력을 받음
    if input_sentence.lower() == '종료':
        break  # 입력이 '종료'라면 루프를 종료
    response = chatbot.levenshtein_Distance_answer(input_sentence)  # 레벤슈타인 거리기반 답변 생성
    print('Chatbot:', response)  # 챗봇의 응답을 출력