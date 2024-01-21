
# import random
# import time
#
# def generate_math_question():
#     # Types of operations
#     operations = ['+', '-', '*', '/']
#     operation = random.choice(operations)
#
#     # Generating two random numbers
#     num1 = random.randint(1, 10)
#     num2 = random.randint(1, 10)
#
#     # Creating the question
#     if operation == '/':  # To avoid division by zero
#         num2 = random.randint(1, 10)
#         question = f"{num1} {operation} {num2}"
#         answer = num1 / num2
#     else:
#         question = f"{num1} {operation} {num2}"
#         answer = eval(question)
#
#     # Formatting the question and answer
#     return question, round(answer, 2)
#
# def countdown(seconds):
#     for i in range(seconds, 0, -1):
#         print(i)
#         time.sleep(1)
#
# def ask_math_question():
#     q, a = generate_math_question()
#     print(f"Question: {q} = ?")
#     countdown(3)
#     print(f"Answer: {a}\n")
#
# # 계산 문제를 출력하고 사용자가 입력한 답을 판별하는 함수
# def execute_math_question(question, answer):
#
#     print(f"\r\n문제: {question}= ?\n")
#
#
#     start_time = time.time()  # 시작 시간 기록
#
#     user_answer = int(input("정답을 입력하세요: "))
#
#     end_time = time.time()  # 사용자가 대답한 시간 기록
#     elapsed_time = end_time - start_time  # 경과 시간 계산
#
#     # 사용자의 답이 맞고 시간도 지켰을 때
#     if user_answer == answer and elapsed_time <= 3:
#         print("\n정답입니다^^!")
#
#     # 답은 맞았으나 시간이 초과
#     elif user_answer == answer and elapsed_time > 3:
#         print("\n답은 맞았는데.. 시간 초과입니다.")
#
#     # 시간은 지켰는데 답은 틀림
#     elif user_answer != answer and elapsed_time <= 3:
#         print("\n오답")
#
#     # 답도 틀리고 시간도 못지킴
#     else:
#         print("\n오답")
#
#     # 소요 시간 출력, 소숫점 3째자리에서 반올림
#     print(f"소요시간: {round(elapsed_time, 2)} 초")
#
#
#
# # 5개의 계산 문제가 출력
# print("5개의 계산 문제가 출력됩니다. 제한 시간은 3초입니다. 행운을 빕니다.\n")
# time.sleep(2)
#
# # 5개의 문제가 for 루프를 통해 출력됨
# for _ in range(5):
#     q, a = generate_math_question()
#     execute_math_question(q, a)

