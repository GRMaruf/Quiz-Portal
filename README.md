# Quiz Portal

A role-based quiz platform where quiz makers create and manage quizzes, and participants take them — built with Django. Quiz makers can also switch into participant mode to test their own quizzes before publishing.

🔗 **Live demo:** https://quiz.pybrothers.top/

- Quiz Maker - `username: sara` and `password: demo123`
- Participant - `username: lucy` and `password: demo123`

<img width="1357" height="679" alt="create quiz" src="https://github.com/user-attachments/assets/c6c08d15-a4c8-4371-a61d-a31e05593d58" />

<img width="1359" height="683" alt="create questions" src="https://github.com/user-attachments/assets/c1a082bc-0687-4542-9306-0d02c4b499dc" />

<img width="1359" height="702" alt="all quizes" src="https://github.com/user-attachments/assets/f5271f7e-5626-47b9-b573-3ed6b3f6a71d" />

<img width="1347" height="633" alt="leaderboard" src="https://github.com/user-attachments/assets/780332c6-75ac-47c9-87d0-03395cb8c39e" />

## Features
- Role-based authentication (Quiz Maker vs Participant)
- Quiz makers can create, edit, and manage quizzes and questions
- Quiz makers can preview/take their own quizzes before publishing
- Participants can browse and attempt available quizzes
- Automatic scoring with a leaderboard/ranking system

## Tech Stack
Python · Django · SQLite/PostgreSQL · HTML/CSS/Bootstrap

## Run Locally
```bash
git clone https://github.com/GRMaruf/Quiz-Portal.git
cd Quiz-Portal
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## What I'd Build Next
- Timed quizzes with auto-submit
- Multiple question types (currently single-choice only)
- Export results as CSV/PDF
- Update user experience
