import os
from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Import models and database
from models import db, User, Subject, Chapter, Quiz, Questions, UserAnswers, Score


def init_routes(app):
    """Initialize all routes for the Flask application"""

    # -------------------------------- admin authentication ----------------------------------- #

    @app.route('/adminlogin', methods=['POST'])
    def adminlogin():
        username = request.form['username']
        password = request.form['password']
        admin = User.query.filter_by(Username=username, Password=password, Role='admin').first()
        if admin:
            session['user_id'] = admin.UserID
            session['username'] = admin.Username
            session['role'] = 'admin'
            flash('Admin Login Successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid Admin Credentials!', 'danger')
            return redirect(url_for('home'))
        

    # -------------------------------- User signup , login and logout -------------------------------- #

    @app.route('/usersignup', methods=['POST'])
    def usersignup():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        qualification = request.form['qualification']
        dob = request.form['dob']
        dob = datetime.strptime(dob, "%Y-%m-%d").date()

        existing_user = User.query.filter((User.Username == username) | (User.Email == email)).first()
        if existing_user:   #Cheaking wheather the username or email already exists in database
            flash("Username or Email already exists!", "danger")
            return redirect(url_for("home"))

        new_user = User(
            Username=username, 
            Email=email, 
            Password=password,
            Fullname=fullname,
            Qualification=qualification,
            DOB=dob)
        db.session.add(new_user)
        db.session.commit()
        flash("User Registration Successful! Please Login.", "success")
        return redirect(url_for("home"))

    @app.route('/userlogin', methods=['POST'])
    def userlogin():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(Username=username, Password=password).first()
        if user:
            session['user_id'] = user.UserID
            session['username'] = user.Username
            session['role'] = user.Role
            flash("Login Successful!", "success")
            return redirect(url_for("admin_dashboard" if user.Role == "admin" else "user_dashboard"))
        else:
            flash("Invalid Credentials! Please try again or sign up.", "danger")
            return redirect(url_for("home"))
        

    @app.route('/logout')
    def logout():
        session.clear()
        flash("Logged Out Successfully!", "info")
        return redirect(url_for("home"))

    # -------------------------------- Admin and user Dashboard  -------------------------------- #

    @app.route('/admin_dashboard', methods=['GET'])
    def admin_dashboard():
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized access!", "danger")
            return redirect(url_for("home"))

        query = request.args.get('query', '').strip() #for search query
        users, subjects, quizzes, questions, chapters = [], [], [], [], [] 
        
        if query:  
            users = User.query.filter(User.Username.ilike(f"%{query}%")).all()
            subjects = Subject.query.filter(Subject.Subjectname.ilike(f"%{query}%")).all()
            quizzes = Quiz.query.filter(Quiz.QuizID.ilike(f"%{query}%")).all()
            questions = Questions.query.filter(Questions.Question_statement.ilike(f"%{query}%")).all()
            chapters = Chapter.query.filter(Chapter.Chaptername.ilike(f"%{query}%")).all()  
        else: 
            users = User.query.all()
            subjects = Subject.query.all()
            quizzes = Quiz.query.all()
            questions = Questions.query.all()
            chapters = Chapter.query.all() 

        return render_template("admin_dashboard.html", users=users, subjects=subjects, quizzes=quizzes, questions=questions, chapters=chapters)

    @app.route('/user_dashboard')
    def user_dashboard():
        if 'user_id' not in session or session['role'] != 'user':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        user = User.query.get(session['user_id'])
        query = request.args.get('query', '').strip().lower() #for search query
        today = datetime.today().date() # fetching today's date

        if query:
            subjects = Subject.query.filter(Subject.Subjectname.ilike(f"%{query}%")).all()
        else:
            subjects = Subject.query.all()

        upcoming_quizzes = []
        for subject in subjects:
            chapters = Chapter.query.filter_by(SubjectID=subject.SubjectID).all()
            for chapter in chapters:
                quizzes = Quiz.query.filter_by(ChapterID=chapter.ChapterID).all()
                for quiz in quizzes:
                    quiz_date = quiz.Date_of_quiz  
                    is_expired = quiz_date < today  
                    upcoming_quizzes.append({
                        'quiz': quiz,
                        'chapter': chapter,
                        'subject': subject,
                        'is_expired': is_expired })
                    
        scores = Score.query.filter_by(UserID=user.UserID).all()
        return render_template("user_dashboard.html",user=user,upcoming_quizzes=upcoming_quizzes,subjects=subjects,scores=scores,query=query)

    # -------------------------------- Admin Functionalities -------------------------------- #

    @app.route('/user_info', methods=['GET'])
    def user_info():
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized access!", "danger")
            return redirect(url_for("home"))
        query = request.args.get('query', '').strip()  # Get search query
        users = []
        
        if query:
            users = User.query.filter(User.Username.ilike(f"%{query}%")).all()
        else:
            users = User.query.all()

        return render_template("user_info.html",users=users)

                    # CRUD Subject 

    @app.route('/add_subject', methods=['POST'])
    def add_subject():
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        subject_name = request.form['subject_name']
        description = request.form['description']
        # Creating new subject
        new_subject = Subject(Subjectname=subject_name, Description=description)
        db.session.add(new_subject)
        db.session.commit()

        flash("New Subject Added Successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route('/edit_subject/<int:subject_id>', methods=['POST'])
    def edit_subject(subject_id):
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        subject = Subject.query.get(subject_id)
        if subject:
            subject.Subjectname = request.form['subject_name']
            subject.Description = request.form['description']
            db.session.commit()
            flash("Subject Updated Successfully!", "success")

        return redirect(url_for("admin_dashboard"))

    @app.route('/delete_subject/<int:subject_id>')
    def delete_subject(subject_id):
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        subject = Subject.query.get(subject_id)
        if subject:
            try:
                db.session.delete(subject)
                db.session.commit()
                flash("Subject Deleted Successfully!", "success")
            except IntegrityError:
                db.session.rollback()
                flash("Cannot delete! Remove related chapters or quizzes first.", "danger")

        return redirect(url_for("admin_dashboard"))

                  #CRUD Chapter

    @app.route('/add_chapter', methods=['POST'])
    def add_chapter():
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        subject_id = request.form['subject_id']
        chapter_name = request.form['chapter_name']
        description = request.form['description']

        # Creating new chapter
        new_chapter = Chapter(SubjectID=subject_id, Chaptername=chapter_name, Description=description)
        db.session.add(new_chapter)
        db.session.commit()

        flash("New Chapter Added Successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route('/edit_chapter/<int:chapter_id>', methods=['POST'])
    def edit_chapter(chapter_id):
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        chapter = Chapter.query.get(chapter_id)
        if chapter:
            chapter.Chaptername = request.form['chapter_name']
            chapter.Description = request.form['description']
            db.session.commit()
            flash("Chapter Updated Successfully!", "success")

        return redirect(url_for("admin_dashboard"))

    @app.route('/delete_chapter/<int:chapter_id>')
    def delete_chapter(chapter_id):
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        chapter = Chapter.query.get(chapter_id)
        if chapter:
            try:
                db.session.delete(chapter)
                db.session.commit()
                flash("Chapter Deleted Successfully!", "success")
            except IntegrityError:
                db.session.rollback()
                flash("Cannot delete! Remove related quizzes or questions first.", "danger")

        return redirect(url_for("admin_dashboard"))

                  # CRUD Quiz 

    @app.route('/add_quiz', methods=['POST'])
    def add_quiz():
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        chapter_id = request.form['chapter_id']
        date_of_quiz = request.form['date_of_quiz']
        time_duration = request.form['time_duration']
        remarks = request.form.get('remarks', '')

        # Creating new quiz
        new_quiz = Quiz(ChapterID=chapter_id,Date_of_quiz=datetime.strptime(date_of_quiz, "%Y-%m-%d").date(),Time_duration=time_duration,Remarks=remarks)
        db.session.add(new_quiz)
        db.session.commit()

        flash("New Quiz Added Successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route('/edit_quiz/<int:quiz_id>', methods=['POST'])
    def edit_quiz(quiz_id):
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        quiz = Quiz.query.get(quiz_id)
        if quiz:
            quiz.Date_of_quiz = datetime.strptime(request.form['date_of_quiz'], "%Y-%m-%d").date()
            quiz.Time_duration = request.form['time_duration']
            #quiz.Remarks = request.form['remarks']
            db.session.commit()
            flash("Quiz Updated Successfully!", "success")
        else:
            flash("Quiz Not Found!", "danger")

        return redirect(url_for("admin_dashboard"))

    @app.route('/delete_quiz/<int:quiz_id>', methods=['GET'])
    def delete_quiz(quiz_id):
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        quiz = Quiz.query.get(quiz_id)

        if quiz:
            try:
                UserAnswers.query.filter(UserAnswers.QuestionID.in_(db.session.query(Questions.QuestionID).filter_by(QuizID=quiz_id))).delete(synchronize_session=False)
                Questions.query.filter_by(QuizID=quiz_id).delete()
                Score.query.filter_by(QuizID=quiz_id).delete()
                db.session.delete(quiz)
                db.session.commit()

                flash("Quiz Deleted Successfully!", "success")

            except IntegrityError:
                db.session.rollback()
                flash("Cannot delete! Remove related data first.", "danger")
        else:
            flash("Quiz Not Found!", "danger")

        return redirect(url_for("admin_dashboard"))

             #CRUD Question 

    @app.route('/add_question', methods=['POST'])
    def add_question():
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        question_statement = request.form['question_statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option_index = request.form['correct_option'] 
        quiz_id = request.form['quiz_id']
        
        correct_option = [option1, option2, option3, option4][int(correct_option_index) - 1]

        new_question = Questions(Question_statement=question_statement, Option1=option1,Option2=option2,Option3=option3,Option4=option4,Correct_option=correct_option,QuizID=quiz_id)
        db.session.add(new_question)
        db.session.commit()
        flash("New Question Added Successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route('/edit_question/<int:question_id>', methods=['POST'])
    def edit_question(question_id):
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        question = Questions.query.get(question_id)
        if not question:
            flash("Question not found!", "danger")
            return redirect(url_for("admin_dashboard"))

        question.Question_statement = request.form['question_statement']
        question.Option1 = request.form['option1']
        question.Option2 = request.form['option2']
        question.Option3 = request.form['option3']
        question.Option4 = request.form['option4']
        
        correct_option_index = request.form['correct_option']
        question.Correct_option = [question.Option1, question.Option2, question.Option3, question.Option4][int(correct_option_index) - 1]

        db.session.commit()
        flash("Question Updated Successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route('/delete_question/<int:question_id>')
    def delete_question(question_id):
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized Access!", "danger")
            return redirect(url_for("home"))

        question = Questions.query.get(question_id)
        
        if not question:
            flash("Question not found!", "danger")
        else:
            UserAnswers.query.filter_by(QuestionID=question_id).delete()
            db.session.delete(question)
            db.session.commit()
            flash("Question Deleted Successfully!", "success")

        return redirect(url_for("admin_dashboard"))

    # -------------------------------- User Functionalities --------------------------------- #

    @app.route('/start_quiz/<int:quiz_id>')
    def start_quiz(quiz_id):
        if 'user_id' not in session:
            flash("Please log in first.", "danger")
            return redirect(url_for("home"))

        quiz = Quiz.query.get_or_404(quiz_id)
        today = datetime.today().date()  
        # Prevents the user to take quiz if due date is passed
        if quiz.Date_of_quiz < today:
            flash("This quiz is no longer available.", "danger")
            return redirect(url_for("user_dashboard"))

        questions = Questions.query.filter_by(QuizID=quiz_id).all()

        if not questions:
            flash("No questions found for this quiz.", "danger")
            return redirect(url_for("user_dashboard"))

        session['quiz_id'] = quiz_id
        session['current_question'] = 0  
        session['user_answers'] = {}  

        return redirect(url_for('next_question'))

    @app.route('/next_question', methods=['POST', 'GET'])
    def next_question():
        if 'quiz_id' not in session:
            flash("Quiz session expired. Please start again.", "danger")
            return redirect(url_for("user_dashboard"))

        quiz_id = session['quiz_id']
        current_question_index = session['current_question']
        questions = Questions.query.filter_by(QuizID=quiz_id).all()
        # redirects to submit it all questions are answered
        if current_question_index >= len(questions):
            return redirect(url_for("submit_quiz", quiz_id=quiz_id))

        question = questions[current_question_index]
        total_questions = len(questions)
        quiz = Quiz.query.get(quiz_id)  

        return render_template("quiz_attempt.html",quiz=quiz,quiz_id=quiz_id,question=question,current_question=current_question_index + 1,total_questions=total_questions,)

    @app.route('/save_answer', methods=['POST'])
    def save_answer():
        if 'quiz_id' not in session:
            flash("Quiz session expired. Please start again.", "danger")
            return redirect(url_for("user_dashboard"))

        selected_answer = request.form.get("selected_answer")
        question_id = request.form.get("question_id")

        if 'user_answers' not in session:
            session['user_answers'] = {}

        if question_id and selected_answer:
            session['user_answers'][str(question_id)] = selected_answer 
        session.modified = True  
        #moving to next question 
        session['current_question'] += 1
        quiz_id = session['quiz_id']
        total_questions = Questions.query.filter_by(QuizID=quiz_id).count()

        if session['current_question'] >= total_questions:
            return redirect(url_for("submit_quiz", quiz_id=quiz_id))

        return redirect(url_for("next_question"))

    @app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
    def submit_quiz(quiz_id):
        if 'user_id' not in session:
            flash("Please log in to submit the quiz.", "danger")
            return redirect(url_for('home'))

        user_id = session['user_id']
        quiz = Quiz.query.get_or_404(quiz_id)
        questions = Questions.query.filter_by(QuizID=quiz_id).all()
        last_question_id = request.form.get("question_id")
        last_answer = request.form.get("selected_answer")

        if 'user_answers' not in session:
            session['user_answers'] = {}

        if last_question_id and last_answer:
            session['user_answers'][str(last_question_id)] = last_answer 

        session.modified = True  
        score = 0
        for question in questions:
            question_id = str(question.QuestionID)  
            submitted_answer = session['user_answers'].get(question_id, None)
            correct_answer = question.Correct_option

            if submitted_answer == correct_answer:
                score += 1  

        total_questions = len(questions)
        final_score = (score / total_questions) * 100
        print(f"DEBUG: User {user_id}, Correct Answers: {score}, Total Questions: {total_questions}, Final Score: {final_score}")
        new_score = Score(QuizID=quiz_id, UserID=user_id, TotalScore=final_score)
        db.session.add(new_score)
        db.session.commit()
        
        for question_id, selected_answer in session['user_answers'].items():
            new_answer = UserAnswers(ScoreID=new_score.ScoreID,QuestionID=int(question_id),SelectedAnswer=selected_answer)
            db.session.add(new_answer)
        db.session.commit()

        session.pop('quiz_id', None)
        session.pop('current_question', None)
        session.pop('user_answers', None)

        flash(f"Quiz submitted! Your score: {final_score:.2f}%", "success")
        response = redirect(url_for('user_dashboard'))
        response.set_cookie(f'quiz_timer_{quiz_id}', '', expires=0) 
        return response

    @app.route('/user_scores')
    def user_scores():
        if 'user_id' not in session:
            flash("Unauthorized access!", "danger")
            return redirect(url_for("home"))

        user_id = session['user_id']
        scores = Score.query.filter_by(UserID=user_id).all()
        
        for score in scores:
            score.retake_allowed = score.TotalScore < 40 
            ist_time = score.TimeStamp + timedelta(hours=5, minutes=30)  # Converting the time to IST
            score.ist_time_str = ist_time.strftime('%d-%m-%Y %H:%M:%S')  

        return render_template("quiz_scores.html", scores=scores)

    # -------------------------------- Summary Charts --------------------------------- #

    @app.route('/admin_summary')
    def admin_summary():
        if 'user_id' not in session or session['role'] != 'admin':
            flash("Unauthorized access!", "danger")
            return redirect(url_for("home"))

        generate_admin_summary()
        return render_template("admin_summary.html")

    @app.route('/user_summary')
    def user_summary():
        if 'user_id' not in session or session['role'] != 'user':
            flash("Unauthorized access!", "danger")
            return redirect(url_for("home"))

        user_id = session['user_id']
        generate_user_summary(user_id)
        return render_template("user_summary.html")

    @app.route('/serve_chart/<filename>')
    def serve_chart(filename):
        return send_from_directory("static", filename)

    # -------------------------------- API endpoints  --------------------------------- #

    @app.route('/api/subjects', methods=['GET'])
    def get_subjects():
        subjects = Subject.query.all()
        subjects_data = [{'SubjectID': subject.SubjectID,'Subjectname': subject.Subjectname,'Description': subject.Description} for subject in subjects]
        return jsonify({'subjects': subjects_data})

    @app.route('/api/chapters/<int:subject_id>', methods=['GET'])
    def get_chapters(subject_id):
        chapters = Chapter.query.filter_by(SubjectID=subject_id).all()
        if not chapters:
            return jsonify({'error': 'No chapters found for this subject'}), 404
        
        chapters_data = [{'ChapterID': chapter.ChapterID,'Chaptername': chapter.Chaptername,'Description': chapter.Description} for chapter in chapters]
        return jsonify({'chapters': chapters_data})

    @app.route('/api/quizzes/<int:chapter_id>', methods=['GET'])
    def get_quizzes(chapter_id):
        quizzes = Quiz.query.filter_by(ChapterID=chapter_id).all()
        if not quizzes:
            return jsonify({'error': 'No quizzes found for this chapter'}), 404
        
        quizzes_data = [{'QuizID': quiz.QuizID,'ChapterID': quiz.ChapterID,'Date_of_quiz': quiz.Date_of_quiz,'Time_duration': quiz.Time_duration} for quiz in quizzes]
        return jsonify({'quizzes': quizzes_data})

    @app.route('/api/scores/<int:user_id>', methods=['GET'])
    def get_scores(user_id):
        scores = Score.query.filter_by(UserID=user_id).all()
        if not scores:
            return jsonify({'error': 'No scores found for this user'}), 404
        
        scores_data = [{'ScoreID': score.ScoreID,'QuizID': score.QuizID,'TotalScore': score.TotalScore,'Timestamp': score.TimeStamp.strftime('%Y-%m-%d %H:%M:%S') } for score in scores]
        return jsonify({'scores': scores_data})

    @app.route("/")
    def home():
        return render_template("index.html")


def generate_admin_summary():
    users = User.query.all()
    quizzes = Quiz.query.all()
    scores = Score.query.all()
    
    user_names = [user.Username for user in users]    # User participation chart
    user_scores = [Score.query.filter_by(UserID=user.UserID).count() for user in users]
    
    plt.figure(figsize=(8, 5))
    plt.barh(user_names, user_scores, color='blue')
    plt.xlabel("Number of Quizzes Taken")
    plt.ylabel("User Name")
    plt.title("User Participation in Quizzes")
    plt.savefig("static/admin_user_participation.png")
    plt.close()
    
    quiz_names = [quiz.Remarks if quiz.Remarks else f"Quiz {quiz.QuizID}" for quiz in quizzes]       # Quiz statistics chart
    quiz_attempts = [Score.query.filter_by(QuizID=quiz.QuizID).count() for quiz in quizzes]
    plt.figure(figsize=(8, 5))
    plt.bar(quiz_names, quiz_attempts, color='green')
    plt.xlabel("Quiz Name")
    plt.ylabel("Number of Attempts")
    plt.title("Quiz Attempt Statistics")
    plt.xticks(rotation=45, ha='right')
    plt.savefig("static/admin_quiz_statistics.png")
    plt.close()


def generate_user_summary(user_id):
    scores = Score.query.filter_by(UserID=user_id).all()
    IST_OFFSET = timedelta(hours=5, minutes=30)
    chapter_scores = {}
    for score in scores:
        chapter_name = score.quiz.chapter.Chaptername if score.quiz.chapter else f"Quiz {score.QuizID}"
        ist_time = score.TimeStamp + IST_OFFSET  # Converting to IST

        if chapter_name not in chapter_scores:
            chapter_scores[chapter_name] = []
        chapter_scores[chapter_name].append((ist_time, score.TotalScore))
    
    plt.figure(figsize=(12, 6))

    for chapter, data in chapter_scores.items():
        timestamps, scores = zip(*sorted(data))  # Sorting by timestamp
        plt.plot(timestamps, scores, marker='o', linestyle='-', label=chapter)
    
    plt.xlabel("Time (IST)")
    plt.ylabel("Score (%)")
    plt.title("User Performance Over Time by Chapter")
    plt.legend(title="Chapters", loc="upper left", bbox_to_anchor=(1,1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y, %H:%M'))  # Storing in this type of format "03 Mar 2025, 14:30"
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator()) 
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("static/user_performance_chart.png")
    plt.close()
