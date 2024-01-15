# 추가할 기능
# 문제 맞추면 포인트 지급, 문제 풀 시 3초 제한. 3, 2, 1 메세지 띄우기
# 나누기 소수점 안나오게

import random

def generate_math_question():
    # Types of operations
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)

    # Generating two random numbers
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    # Creating the question
    if operation == '/':  # To avoid division by zero
        num2 = random.randint(1, 10)
        question = f"{num1} {operation} {num2}"
        answer = num1 / num2
    else:
        question = f"{num1} {operation} {num2}"
        answer = eval(question)

    # Formatting the question and answer
    return question, round(answer, 2)

# Example: Generate 5 random math questions
for _ in range(5):
    q, a = generate_math_question()
    print(f"Question: {q} = ?\nAnswer: {a}\n")

