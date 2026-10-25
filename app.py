
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from models import db, User, Question, QuizResult

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]


db.init_app(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

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
    },


    {
        "id": 11,
        "question": "What is cloud computing?",
        "options": [
            "Building physical computers",
            "Delivering computing services over the internet",
            "Storing files only on local hard drives",
            "Creating websites without servers"
        ],
        "answer": "Delivering computing services over the internet"
    },
    {
        "id": 12,
        "question": "What is the main purpose of Amazon S3?",
        "options": [
            "Running virtual machines",
            "Managing user permissions",
            "Storing and retrieving objects",
            "Monitoring CPU performance"
        ],
        "answer": "Storing and retrieving objects"
    },
    {
        "id": 13,
        "question": "What does SaaS stand for?",
        "options": [
            "Storage as a Service",
            "Software as a Service",
            "Security as a System",
            "Server as a Software"
        ],
        "answer": "Software as a Service"
    },
    {
        "id": 14,
        "question": "What is an AWS Region?",
        "options": [
            "A single virtual server",
            "A geographical area containing AWS infrastructure",
            "A security group",
            "A type of database"
        ],
        "answer": "A geographical area containing AWS infrastructure"
    },
    {
        "id": 15,
        "question": "What is an AWS Availability Zone?",
        "options": [
            "A billing account",
            "A software application",
            "An isolated infrastructure location within a Region",
            "A storage bucket"
        ],
        "answer": "An isolated infrastructure location within a Region"
    }
    
]


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or len(password) < 8:
            flash("Enter a username, email and password of at least 8 characters.")
            return render_template("register.html")

        existing_user = db.session.scalar(
            select(User).where(
                (User.username == username) | (User.email == email)
            )
        )

        if existing_user:
            flash("Username or email is already registered.")
            return render_template("register.html")

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = db.session.scalar(
            select(User).where(User.email == email)
        )

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("home"))

        flash("Invalid email or password.")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/")
@login_required
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
@login_required
def submit():
    score = 0

    for question in questions:
        user_answer = request.form.get(str(question["id"]))

        if user_answer == question["answer"]:
            score += 1

    # Create a quiz result for the logged-in user
    result = QuizResult(
        user_id=current_user.id,
        score=score,
        total_questions=len(questions)
    )

    # Save the result to PostgreSQL
    db.session.add(result)
    db.session.commit()            

    return render_template(
        "result.html",
        score=score,
        total=len(questions)
    )


@app.route("/history")
@login_required
def history():
    results = (
        QuizResult.query
        .filter_by(user_id=current_user.id)
        .order_by(QuizResult.played_at.desc(), QuizResult.id.desc())
        .all()
    )

    return render_template(
        "history.html",
        results=results
    )


@app.route("/leaderboard")
@login_required
def leaderboard():
    # Get results and their associated users
    results = QuizResult.query.all()

    # Store each player's best result
    best_results = {}

    for result in results:
        user_id = result.user_id
        percentage = (
            result.score / result.total_questions * 100
        )

        if (
            user_id not in best_results
            or percentage > best_results[user_id]["percentage"]
        ):
            best_results[user_id] = {
                "username": result.user.username,
                "score": result.score,
                "total": result.total_questions,
                "percentage": percentage
            }

    rankings = sorted(
        best_results.values(),
        key=lambda player: player["percentage"],
        reverse=True
    )

    return render_template(
        "leaderboard.html",
        rankings=rankings
    )



if __name__ == "__main__":
    app.run(debug=False)
