
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
    },

    {
        "id": 5,
        "question": "What does the '2' in EC2 stand for?",
        "options": [
            "Elastic Compute Cloud (Two Cs)",
            "Second Generation Cloud",
            "Dual Core Processor",
            "Two Factor Authentication"
        ],
        "answer": "Elastic Compute Cloud (Two Cs)"
    },

    {
        "id": 6,
        "question": "Which EC2 purchasing option offers up to a 90% discount by utilizing spare AWS capacity?",
        "options": [
            "On-Demand Instances",
            "Reserved Instances",
            "Dedicated Hosts",
            "Spot Instances"
        ],
        "answer": "Spot Instances"
    },


    {
        "id": 7,
        "question": "What AWS hardware innovation offloads networking and storage tasks to give EC2 instances near bare-metal performance?",
        "options": [
            "AWS Nitro System",
            "Amazon Xen Hypervisor",
            "AWS Outposts",
            "Amazon Elastic Block Store"
        ],
        "answer": "AWS Nitro System"
    },


    {
        "id": 8,
        "question": "In the EC2 instance name 'm6g.xlarge', what does the 'g' represent?",
        "options": [
            "General Purpose",
            "Graphics Optimization",
            "Amazon Graviton Processor",
            "Gigabit Networking"
        ],
        "answer": "Amazon Graviton Processor"
    },


    {
        "id": 9,
        "question": "Which foundational cloud service model provides users with direct access to virtual machines and networking infrastructure?",
        "options": [
            "SaaS (Software as a Service)",
            "PaaS (Platform as a Service)",
            "IaaS (Infrastructure as a Service)",
            "FaaS (Function as a Service)"
        ],
        "answer": "IaaS (Infrastructure as a Service)"
    },

    {
        "id": 10,
    "question": "What is the name of the persistent block storage service typically used as the primary hard drive for an EC2 instance?",
    "options": [
        "Amazon S3",
        "Amazon EBS (Elastic Block Store)",
        "Amazon EFS (Elastic File System)",
        "Amazon Instance Store"
    ],
    "answer": "Amazon EBS (Elastic Block Store)"
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
