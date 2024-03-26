# Adventura

Play this puzzle at - [http://zeon3099.pythonanywhere.com/signin](http://zeon3099.pythonanywhere.com/signin)

## Overview

This puzzle assesses the following skills:

- **Analytical Thinking:** The puzzle requires the user to analyze clues and piece them together logically.
- **Attention to Detail:** Close observation and concentration are needed to identify intricate details.
- **Critical Thinking:** Logical reasoning is essential to evaluate information and make informed decisions.
- **Adaptability:** The solution may change as new information is uncovered.
- **Time Management:** Solving the puzzle within a designated time frame demonstrates effective time management.

## Possible Solution

The only possible way to solve it is: west, west, north, north, east, west.

## Deadends

All other options except the correct answers are deadends and are penalized with a 5-second time penalty for each wrong answer or refresh during the assessment.

## Setup Instructions

1. Ensure Python is updated and install the following dependencies:

```bash
pip install Flask-SQLAlchemy
pip install hashlib
pip install Flask
```

2. Navigate to the project directory in the terminal.
3. Run the following command to start the server:

```bash
python app.py
```
4. Access the application through a web browser using the provided link.

## Features

- **Progress Persistence:** On refreshing the page, the puzzle restarts from the same step or provides the option to restart.
- **Admin Dashboard:** Allows tracking and analysis of user progress, including time recorded for each question, penalty for wrong answers, and sorting users by overall score.
- **User Leaderboard:** Displays the overall score of top users.
- **Admin Login:** Secret key authentication for admin access. Secret key: "as"
- **View All Admins:** Option to view usernames of all admins.
- **Database Reset:** Visit "zeon3099.pythonanywhere.com/reset" to reset all databases.


