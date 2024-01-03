import random

def generate_math_question():
    # Types of operations
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)

    # Generating two random numbers
    num1 = random.randint(50, 1000)
    num2 = random.randint(50, 1000)

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
