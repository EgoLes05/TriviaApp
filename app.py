
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask_migrate import Migrate
from models import db, User, Question, QuizResult

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

db.init_app(app)
migrate = Migrate(app, db)

questions = [
    {
        "id": 1,
        "question": "What does AWS stand for?",
        "options": [
            "Amazon Web Services",
            "Advanced Web System",
            "Amazon Website Server",
            "Automated Web Services"
        ],
        "answer": "Amazon Web Services"
    },
    {
        "id": 2,
        "question": "Which language is Flask built with?",
        "options": ["Java", "Python", "C++", "JavaScript"],
        "answer": "Python"
    },
    {
        "id": 3,
        "question": "Which AWS service provides virtual servers?",
        "options": ["S3", "Lambda", "EC2", "RDS"],
        "answer": "EC2"
    },
    {
        "id": 4,
        "question": "What does HTTP stand for?",
        "options": [
            "HyperText Transfer Protocol",
            "High Transfer Text Process",
            "Hyper Tool Transfer Program",
            "Host Transfer Protocol"
        ],
        "answer": "HyperText Transfer Protocol"
    }
]


@app.route("/")
def home():
    public_questions = [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in questions
    ]
    return render_template("index.html", questions=public_questions)


@app.route("/submit", methods=["POST"])
def submit():
    score = 0

    for question in questions:
        user_answer = request.form.get(str(question["id"]))

        if user_answer == question["answer"]:
            score += 1

    return render_template(
        "result.html",
        score=score,
        total=len(questions)
    )


if __name__ == "__main__":
    app.run(debug=True)
