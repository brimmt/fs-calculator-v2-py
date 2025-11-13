import os
import openai
import random
from fastapi import APIRouter, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from rate_limit import limiter

router = APIRouter()
load_dotenv()

openai.api_key = os.getenv("OpenAI_API_KEY")


class quizAnswer(BaseModel):
    question: str
    user_answer: str
    correct_answer: float


operations = ["add", "subtract", "multiply", "divide", "power"]


@limiter.limit("10/second")
@router.get("/quiz")
def generate_question(request: Request):

    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(operations)

    prompt = f"Write a single math question asking the user to {operation} {num1} and {num2}. Keep it short."

    try:

        completion = openai.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
        )
        question_text = completion.choices[0].message.content.strip()
    except Exception:
        symbols = {
            "add": "+",
            "subtract": "-",
            "multiply": "×",
            "divide": "÷",
            "power": "**",
        }
        question_text = f"What is {num1} {symbols[operation]} {num2}?"

    if operation == "add":
        answer = num1 + num2
    elif operation == "subtract":
        answer = num1 - num2
    elif operation == "multiply":
        answer = num1 * num2
    elif operation == "divide":
        answer = round(num1 / num2, 2)
    elif operation == "power":
        answer = num1**num2

    return {"question": question_text, "correct_answer": answer}


@router.post("/quiz/answer")
def check_answer(payload: quizAnswer):
    try:
        user = float(payload.user_answer)
        correct = float(payload.correct_answer)

        if abs(user - correct) < 0.01:
            feedback = "Correct! Great job."
        else:
            feedback = f"Incorrect. The correct answer was {correct}."

        explanation_prompt = (
            f"Explain step-by-step how to solve this math question: '{payload.question}'. "
            f"The correct answer is {correct}. Keep the explanation short and beginner-friendly."
        )

        try:
            completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": explanation_prompt}],
                max_tokens=100,
            )
            explanation = completion.choices[0].message.content.strip()
        except Exception:
            explanation = "Explanation not available right now."

    except ValueError:
        feedback = "Please enter a numeric answer."
        explanation = ""
    except Exception:
        feedback = "An error occurred while checking your answer."
        explanation = ""

    return {"feedback": feedback, "explanation": explanation}
