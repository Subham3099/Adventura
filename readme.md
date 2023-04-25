------------------------------------------------------readme----------------------------------------


# Play this puzzle at - http://zeon3099.pythonanywhere.com/signin

# This puzzle assesses the following things:

->Analytical thinking: The puzzle requires the user to analyze the clues and piece them together to form a solution. 
The ability to analyze information thoroughly and logically is a crucial aspect of analytical thinking and can be 
used in problem-solving and decision-making.

->Attention to detail: The puzzle may contain intricate details that 
require close observation and concentration to identify. A user's attention 
to detail can display their ability to identify minor issues, analyze information 
thoroughly, and complete tasks accurately.

->Critical thinking: Critical thinking involves the use of logic 
and reasoning to evaluate information and make informed decisions. 
Solving the puzzle requires critical thinking to determine the sequence of 
steps required to solve it, providing insights into the individual's critical thinking skills.

->Adaptability: The puzzle may contain unexpected or unanticipated elements, 
and sometimes the solution may change as new information is uncovered. 
A user's ability to adapt and adjust to a changing situation can exhibit their flexibility and agility.

->Time management: Solving the puzzle within a designated time frame requires effective time management skills. 
A user's ability to prioritize tasks, focus on important elements of the puzzle, and manage their time appropriately 
can exhibit their time management skills.


# Possible Ways to Solve The Puzzle :
-> There is only one possible way to solve it that is : west,west,north,north,east,west

# Deadends:
-> All other options except correct answers are deadends and are given a penalty of 5 seconds for each wrong answer or refresh during the assessment.

# Steps to set up the Project
->python should be updated and following should be there in system if not install them using :
pip install Flask-SQLAlchemy
pip install hashlib
pip install Flask

->Goto directory of the application on terminal and give command "python app.py"
->There it will show a link goto that link for local hosting of this application.
->For additional requirements for runtime environment it is given in requirements.txt

# Implemented and Extra Features :

->On refreshing, from either browser or website, the puzzle  starts from the same step or give the user an option to restart.
->A dashboard for the admin where the progress of all the users can be tracked & analyzed is there. There is time recorded for each question answered by the user 
	and the penalty for wrong answers and overall list is sorted by descending order of overall score.
->User Leaderboard : it only shows the overall score of the top users.
->Admin login with secret key : There is also an option to add Admins with the help of the secret key - "as" .
->View all Admins : there is also an option to view the usernames of all admins of the game.
->To reset all databases goto : "zeon3099.pythonanywhere.com/ reset"

