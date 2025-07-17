Absolutely! Here's the revised **README.md** with the requested changes:

---

# 🧠 Quiz Master - V2

**Quiz Master V2** is a full-stack exam preparation web application built as part of the *Modern Application Development II* course. It supports **Admin (Quiz Master)** and **User** roles. The admin can create and manage subjects, chapters, quizzes, and users, while users can register, attempt quizzes, view scores, and receive automatic email reports and reminders.

---

## 🔑 Key Features

### 👨‍🏫 Admin (Quiz Master)

* Predefined admin account (no registration)
* CRUD operations for:

  * Subjects
  * Chapters
  * Quizzes
  * Questions
* Schedule quizzes with time limits
* View all users and their performance
* View charts and analytics
* Daily and monthly task automation (via Celery)

### 👩‍🎓 User

* Register and login (JWT-secured)
* View subjects, chapters, and available quizzes
* Attempt quizzes with countdown timer
* Get instant score feedback
* View history of past quiz attempts
* Export personal quiz history as CSV
* Receive:

  * Daily reminders for pending quizzes
  * Monthly activity reports by email

---

## ⚙️ Technologies Used

### Backend

* **Flask** – REST API development
* **Flask-JWT-Extended** – Token-based authentication
* **Flask-SQLAlchemy** – ORM for SQLite
* **Celery + Redis** – Asynchronous background jobs

### Frontend

* **Vue.js** – User interface
* **Bootstrap** – UI styling
* **HTML5/JS** – Form validations and responsiveness

### Others

* **SQLite** – Relational database
* **MailHog** – Development SMTP server for testing emails
* **Redis** – Caching and message broker for Celery

---

## ⚙️ Setup Instructions

### 🔁 1. Backend Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd quiz-master-v2/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

Flask API will be available at:
➡️ `http://127.0.0.1:5000/`

---

### 🌐 2. Frontend Setup (VueJS)

```bash
# In a new terminal
cd frontend/quiz_master/

# Install Node.js dependencies
npm install

# Run the VueJS development server
npm run dev
```

Frontend will be available at:
➡️ `http://localhost:8080/`

---

### 🧠 3. Redis Setup

```bash
# Install Redis server
sudo apt install redis-server

# Start Redis server
sudo systemctl start redis-server

# To stop Redis
sudo systemctl stop redis-server

# To check Redis status
sudo systemctl status redis-server
```

---

### ✉️ 4. MailHog Setup (SMTP for Dev Emails)

```bash
# Install Go language
sudo apt-get -y install golang-go

# Install MailHog
go install github.com/mailhog/MailHog@latest

# Run MailHog
~/go/bin/MailHog
```

Access MailHog UI at:
➡️ `http://localhost:8025/`

---

### ⏱️ 5. Celery Workers & Beat Scheduler

Start in **two new terminals** from project root:

```bash
# Terminal 1 - Celery Worker
celery -A tasks.celery worker --loglevel=info

# Terminal 2 - Celery Beat Scheduler
celery -A tasks.celery beat --loglevel=info
```

---

### 🔗 6. Celery Test Routes (Demo)

To test the Celery-based email tasks manually:

* **Daily Reminder**:
  [http://localhost:5000/test-daily](http://localhost:5000/test-daily)

* **Monthly Report**:
  [http://127.0.0.1:5000/test-monthly](http://127.0.0.1:5000/test-monthly)


---

## 🎥 Video Demonstration

A complete walkthrough of the Quiz Master - V2 application is available in the demo video below:

👉 [Watch Video Demonstration](https://drive.google.com/file/d/1yhqRnPmN1RqMP9E8jFhoAJslVH-vIVbV/view?usp=sharing)

This video covers:

* Project overview and objectives
* Key features for both Admin and User roles
* Demonstration of quiz attempt, result viewing, and Celery-based scheduled tasks
* Frontend and backend integration highlights

---

## 📝 Contact

**Astitva Agarwal**
Student, IITM BS Degree Program
Course: Modern Application Development - II
Project: Quiz Master - V2
Email: *\[[astitvaag2005@gmail.com](mailto:astitvaag2005@gmail.com)]*

Student Email: *\[[23f2004131@ds.study.iitm.ac.in](mailto:23f2004131@ds.study.iitm.ac.in)]*

