from fastapi import FastAPI
from calculator_logic import Calculate
from fastapi.middleware.cors import CORSMiddleware
from ai_logic import router as ai_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Server is running!"}


app.include_router(ai_router)


@app.get("/calculate")
def calculate(num1: int, num2: int, operation: str):
    calc = Calculate(num1, num2)

    if operation == "add":
        result = calc.add()
    elif operation == "subtract":
        result = calc.subtract()
    elif operation == "multiply":
        result = calc.multiply()
    elif operation == "divide":
        result = calc.divide()
    elif operation == "power":
        result = calc.power()
    else:
        return "Invalid operator"

    return {"result": result}
