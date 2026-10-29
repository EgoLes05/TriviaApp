WTC-RUNJ96UV

# ☁️ TriviaApp — Flask Trivia Website Deployed on AWS EC2

**A cloud-hosted trivia application built with Python, Flask, and PostgreSQL, deployed on an Ubuntu-based AWS EC2 instance with Nginx, Gunicorn, HTTPS, and automated TLS certificate renewal.**

[![Python](https://img.shields.io/badge/Python-Flask-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonwebservices&logoColor=white)](https://aws.amazon.com/ec2/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![HTTPS](https://img.shields.io/badge/HTTPS-Let's%20Encrypt-brightgreen)](https://letsencrypt.org/)

**Live demo:** [https://15.240.207.214](https://15.240.207.214) *(available while the EC2 instance is running and the certificate is valid)*  
**Source code:** [github.com/EgoLes05/TriviaApp](https://github.com/EgoLes05/TriviaApp)

---

## 📖 Project overview

TriviaApp is a web-based quiz application that lets users register, log in, answer multiple-choice technology questions, review scores, and compare results on a leaderboard. The questions include cloud computing, AWS, and software-development fundamentals.

The main learning goal was to **take an application from local development to a publicly accessible cloud deployment** and understand the infrastructure needed to run and secure it.

This is a hands-on **cloud engineering portfolio project**, rather than a claim of a fully production-hardened service.

## ✨ Features

- User registration, login, and logout
- Password hashing and authenticated routes using Flask-Login
- Multiple-choice trivia questions covering AWS and other technology topics
- Quiz grading and saved results in PostgreSQL
- Personal quiz history
- Leaderboard based on each user's best percentage score
- HTML templates and CSS styling
- CSRF protection using Flask-WTF
- HTTPS-enabled public deployment

## 🛠️ Technology stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Cloud hosting | AWS EC2 | Virtual server hosting the application |
| Operating system | Ubuntu Linux | Server environment and administration |
| Backend | Python, Flask | Routes, authentication, quiz logic |
| Data storage | PostgreSQL | Persistent user and quiz-result data |
| ORM and migrations | Flask-SQLAlchemy, Flask-Migrate | Database access and schema migrations |
| Application server | Gunicorn | Serves the Flask WSGI application |
| Service management | systemd | Starts and restarts the Gunicorn service |
| Reverse proxy | Nginx | Handles public web requests and forwards them to Gunicorn |
| Networking | AWS Security Groups, Elastic IP | Controls inbound access and provides a stable IPv4 address |
| Transport security | Let's Encrypt, Certbot | TLS certificate issuance and renewal |
| Version control | Git, GitHub | Source control and project sharing |

## 🏗️ Cloud architecture

```mermaid
flowchart TD
    A[Visitor's browser] -->|HTTPS :443| B[AWS EC2 / Ubuntu]
    B --> C[Nginx reverse proxy\nTLS termination]
    C -->|HTTP 127.0.0.1:8000| D[Gunicorn]
    D --> E[Flask TriviaApp]
    E <-->|Database queries| F[(PostgreSQL)]
    G[systemd] -.->|Manages service| D
    H[Certbot + Let's Encrypt] -.->|Certificates and renewal| C
```

**Request flow:** A visitor connects using HTTPS. Nginx terminates TLS and proxies the request to Gunicorn on the server's loopback interface (`127.0.0.1:8000`). Gunicorn runs the Flask app, which processes authentication, questions, scores, and database operations. PostgreSQL stores persistent data.

**Why this matters:** Gunicorn is not directly exposed on a public port; Nginx is the public entry point, and systemd manages the application process.

## 🔐 Security and networking

The deployed configuration uses:

| Port | Protocol | Access / purpose |
| --- | --- | --- |
| `22` | SSH | Restricted to an approved client public IP address |
| `80` | HTTP | Public; redirects ordinary requests to HTTPS and serves ACME validation |
| `443` | HTTPS | Public encrypted website traffic |
| `8000` | Internal HTTP | Gunicorn bound to `127.0.0.1`, not publicly exposed |
| `5432` | PostgreSQL | Not opened in the EC2 public inbound rules |

Additional measures implemented:

- An **Elastic IP** keeps the public web address stable across ordinary instance stop/start cycles while it remains associated.
- **Let's Encrypt certificates** secure browser-to-Nginx traffic.
- **Certbot scheduled renewal** and an Nginx reload hook were tested with a successful renewal dry run.
- **Flask session cookies** use `Secure`, `HttpOnly`, and `SameSite=Lax` in the deployed HTTPS configuration.
- **Database credentials and Flask secrets** are provided through environment variables instead of being hardcoded in application source.
- Flask's interactive debug mode is disabled in the deployed configuration.

> **Note:** HTTPS is one layer of security. Security audits, monitoring, backup/restore testing, IAM hardening, and automated testing are still opportunities for improvement. The certificate is short-lived and continued renewal should be monitored.

## 🗂️ Project structure

```text
TriviaApp/
├── app.py               # Flask routes, authentication, trivia logic
├── models.py            # User, Question, QuizResult models
├── requirements.txt     # Python dependencies
├── migrations/          # Database migration files
├── templates/           # HTML views
├── static/              # CSS and static assets
├── .gitignore
└── README.md
```

## 💻 Run locally

### Prerequisites

- Python 3 and `pip`
- PostgreSQL running locally (or another PostgreSQL instance you can connect to)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/EgoLes05/TriviaApp.git
cd TriviaApp
```

### 2. Create and activate a virtual environment

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows PowerShell:**

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (do **not** commit it):

```dotenv
DATABASE_URL=postgresql+psycopg://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost:5432/trivia_db
SECRET_KEY=REPLACE_WITH_A_LONG_RANDOM_SECRET
```

Create the PostgreSQL database and a user with appropriate permissions before proceeding. Generate your own secret, for example with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Apply database migrations

```bash
python -m flask --app app db upgrade
```

### 6. Start the development server

```bash
python -m flask --app app run --debug
```

Open **http://127.0.0.1:5000** in your browser. The debug flag above is for **local development only**; do not enable it on a public server.

## ☁️ AWS deployment summary

The application was deployed by:

1. Launching an Ubuntu EC2 instance and configuring its Security Group.
2. Connecting over SSH, installing Python, PostgreSQL, Nginx, and required packages.
3. Cloning the GitHub repository and configuring the Python virtual environment, database, and environment variables.
4. Running Flask with **Gunicorn**, bound to `127.0.0.1:8000`.
5. Creating a **systemd** unit (`triviaapp.service`) for reliable application startup and restarts.
6. Configuring **Nginx** as the reverse proxy for incoming website traffic.
7. Associating an **Elastic IP** with the EC2 instance.
8. Issuing an IP-address **Let's Encrypt TLS certificate** using Certbot, configuring HTTPS and HTTP-to-HTTPS redirection.
9. Enabling and testing automated certificate renewal and reloading Nginx after renewal.
10. Enabling secure session-cookie settings in Flask.

Useful server checks:

```bash
sudo systemctl status triviaapp --no-pager
sudo systemctl status nginx --no-pager
sudo nginx -t
curl -I https://15.240.207.214
sudo /snap/bin/certbot certificates
```

> The exact server paths, service definitions, IP-based certificate configuration, and credentials are environment-specific. This section documents the existing deployment rather than providing a one-command deployment script.

## 🧩 Troubleshooting and lessons learned

### Gunicorn port conflict

During deployment, a manually started Gunicorn instance was already listening on `127.0.0.1:8000`. systemd attempted to start another Gunicorn master on the same port, producing `Address already in use` errors and repeated service restarts.

**Resolution:** Identify the listening process using `ss`, inspect service logs using `journalctl`, gracefully stop the conflicting Gunicorn master, and start the systemd-managed service. This reinforced the importance of **process management and observability**, even when a site seems accessible.

### SSH access after networking changes

SSH timed out after the public address changed or connection rules needed review. Checking the instance IP and the source IP allowed by the SSH Security Group helped diagnose connectivity.

### HTTPS certificate lifecycle

Obtained a staging certificate first, then a trusted production certificate for the Elastic IP. Confirmed the Nginx HTTP validation path, the HTTPS endpoint, the HTTP redirect, and the Certbot renewal dry run. Because the IP certificate is short-lived, scheduled renewal and a deploy hook are especially important.

## 🛣️ Next improvements

- [ ] Add automated tests and GitHub Actions CI
- [ ] Add controlled CD to the EC2 instance
- [ ] Monitor application health and logs with Amazon CloudWatch
- [ ] Implement and test PostgreSQL backups and restores
- [ ] Review IAM permissions and remaining deployment security settings
- [ ] Explore Terraform for repeatable cloud infrastructure
- [ ] Add project screenshots and a short YouTube architecture walkthrough

## 🎯 What I learned

This project gave me practical experience in **AWS EC2, Linux administration, SSH, networking, reverse proxies, TLS certificates, application service management, troubleshooting, and deploying a database-backed Python application**. It demonstrates the difference between simply writing an app and maintaining the infrastructure needed to make it available on the internet.

## 👤 Author

**Lesego Mashabela**  
Cloud Engineering student at **WeThinkCode_**  
GitHub: [@EgoLes05](https://github.com/EgoLes05)

---

*Built as a hands-on cloud engineering learning and portfolio project.*
