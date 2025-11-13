const display = document.getElementById("display");
const buttons = document.querySelectorAll(".btn")

let num1 = "";
let num2 = "";
let operation = "";
let isSecondNumber = false;


buttons.forEach((btn) => {
    btn.addEventListener("click", async () => {
        const value = btn.dataset.value;


        if (btn.id === "clear") {
            display.value ="";
            num1 = "";
            num2 = "";
            operation = "";
            isSecondNumber = false;
    
            return;
        }

        if (["+","-","*","/","**"].includes(value)) {
            const operationMap = {
                "+" : "add",
                "-" : "subtract",
                "*" : "multiply",
                "/" : "divide",
                "**": "power"
            };
            operation = operationMap[value];
           isSecondNumber = true;
           display.value += " " + btn.textContent + " ";
           return;
        }


        if (value === "=") {
            if (!num1 || !num2 || !operation) return;

            try {
                const res = await fetch(
                    `http://127.0.0.1:8000/calculate?num1=${num1}&num2=${num2}&operation=${encodeURIComponent(operation)}`
                );

                const data = await res.json();
                display.value = data.result;
                num1 = data.result;
                num2 = "";
                isSecondNumber = false;
            } catch (err) {
                console.error(err);
                display.value = "Error"
            }
            return;
        }
        
        if (!isSecondNumber) {
            num1 += value;
        } else {
            num2 += value;
        }
        display.value += value;

    });
});


// === AI QUIZ MODE ===
const quizBtn = document.getElementById("quiz-btn");
const quizDrawer = document.getElementById("quiz-drawer");
const quizQuestion = document.getElementById("quiz-question");
const quizAnswer = document.getElementById("quiz-answer");
const quizFeedback = document.getElementById("quiz-feedback");
const submitAnswer = document.getElementById("submit-answer");

let currentQuestion = null;
let correctAnswer = null;

// Toggle drawer visibility
quizBtn.addEventListener("click", () => {
  quizDrawer.classList.toggle("active");
  if (quizDrawer.classList.contains("active")) {
    fetchQuizQuestion();
  }
});

// Fetch a new question from backend
async function fetchQuizQuestion() {
  try {
    const res = await fetch("http://127.0.0.1:8000/quiz");
    const data = await res.json();

    currentQuestion = data.question;
    correctAnswer = data.correct_answer;

    quizQuestion.textContent = currentQuestion;
    quizFeedback.textContent = "";
    quizAnswer.value = "";
  } catch (err) {
    console.error(err);
    quizQuestion.textContent = "Error fetching question";
  }
}

// Handle answer submission
submitAnswer.addEventListener("click", async () => {
  if (!quizAnswer.value.trim()) {
    quizFeedback.textContent = "Please enter an answer.";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/quiz/answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: currentQuestion,
        user_answer: quizAnswer.value,
        correct_answer: correctAnswer,
      }),
    });
    const data = await res.json();

    quizFeedback.innerHTML = `
      <strong>${data.feedback}</strong><br/>
      <em>${data.explanation}</em>
    `;

    // Fetch a new question after 2 seconds
    setTimeout(fetchQuizQuestion, 2000);
  } catch (err) {
    console.error(err);
    quizFeedback.textContent = "Error checking answer";
  }
});