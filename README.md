# Quiz Portal

A role-based quiz platform where quiz makers create and manage quizzes, and participants take them — built with Django. Quiz makers can also switch into participant mode to test their own quizzes before publishing.

🔗 **Live demo:** https://quiz.pybrothers.top/

- Quiz Maker - `username: ____` and `password: demo123`
- Participant - `username: ____` and `password: demo123`

[Screenshots here]

## Features
- Role-based authentication (Quiz Maker vs Participant)
- Quiz makers can create, edit, and manage quizzes and questions
- Quiz makers can preview/take their own quizzes before publishing
- Participants can browse and attempt available quizzes
- Automatic scoring with a leaderboard/ranking system

## Tech Stack
Python · Django · SQLite/PostgreSQL · HTML/CSS/Bootstrap

## Run Locally
​```bash
git clone https://github.com/GRMaruf/Quiz-Portal.git
cd Quiz-Portal
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
​```

## What I'd Build Next
- Timed quizzes with auto-submit
- Multiple question types (currently single-choice only)
- Export results as CSV/PDF
- Update user experience
