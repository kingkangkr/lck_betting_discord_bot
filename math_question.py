import random
import time
import threading

def generate_math_question():
    # Types of operations
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)

    # Generating two random numbers
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    # Creating the question
    if operation == '/':
        num1 = num2 * random.randint(1, 10)
        question = f"{num1} {operation} {num2}"
        answer = num1 / num2
    else:
        question = f"{num1} {operation} {num2}"
        answer = eval(question)

    # Formatting the question and answer
    return question, answer



def execute_math_question(question, answer):

    print(f"\r\n문제: {question}= ?\n")


    start_time = time.time()  # 시작 시간 기록

    user_answer = int(input("정답을 입력하세요: "))

    end_time = time.time()  # 사용자가 대답한 시간 기록
    elapsed_time = end_time - start_time  # 경과 시간 계산

    if user_answer == answer and elapsed_time <= 3:
        print("\n정답입니다!")
    elif elapsed_time > 3:
        print("\n시간 초과입니다.")
    else:
        print("\n답 틀렸어요 병신아")

    print(f"소요시간: {round(elapsed_time, 2)} 초")



# 5개의 계산 문제가 출력
print("5개의 계산 문제가 출력됩니다. 제한 시간은 3초입니다. 행운을 빕니다.\n")
time.sleep(2)

for _ in range(5):
    q, a = generate_math_question()
    execute_math_question(q, a)







