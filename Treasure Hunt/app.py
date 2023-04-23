import time
from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import hashlib

app = Flask(__name__, template_folder='templates')
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=30)
db = SQLAlchemy(app)


#user and admin databases
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email    = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    bstime   = db.Column(db.Float(precision=3),default=100.0)

    def __repr__(self):
        return '<User %r>' % self.username
    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adminname = db.Column(db.String(50), unique=True)
    email    = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

    def __repr__(self):
        return '<Admin %r>' % self.adminname

with app.app_context():
    db.create_all()

admin_makekey = "as"


# List of possible questions and answers
questions = [
    ("As you stand on the deck of the ship in the middle of the ocean, you feel the warmth of the sun on your skin and the cool breeze through your hair. The waves are gentle, and the sea is a mesmerizing blue. <br><br>You look through the telescope and find some visions in the following directions :<br><br> North : you see an iceberg in the distance. It's a beautiful sight, with the ice glistening in the sun. It seems to be moving slowly in the water, carried by the ocean currents. You can't see any other landmass or ships in that direction.<br><br>West : you see a small island in the distance . It has a green and lush forest, and the waves are gently crashing onto the white sandy beach. You can also see a few palm trees that sway in the breeze, which makes you feel a little envious. There don't appear to be any signs of other signs of civilization there.<br><br>South : the water seems to stretch forever, and there is only a thin horizon line separating the ocean from the sky. You squint through the telescope and can see some scattered clouds on the horizon, which might indicate rougher seas ahead. You can't pick up any other signs of life or land masses in that direction.<br><br><em>Clue : \"Avast ye! As the sun sets and dives into the briny deep, seek out the path that leads to th' land of the green gown. Thar be unknown dangers and great treasures awaitin' for those brave enough to find 'em. Set sail me hearties! Weigh anchor and hoist the mizzen!\"</em><br> Which direction you would choose : ", 'west'),
    ("As you look out over the island, you see that the island is bordered by the vast blue ocean and has an overall circular shape. The island is divided into three primary areas, separated by varying terrain types.  <br><br>To the North, you see a dense jungle area that extends for miles, with towering trees that create a canopy covering the sky. From your vantage point, you see that the jungle seems to be a primary segment of the island and is the most challenging to navigate through.<br><br>To the West, you see a series of towering cliffs that separate the jungle from a rocky ridge. The rocks in the region are jagged and unforgiving, with rough terrain that is difficult to climb or maneuver through.<br><br>To the East, you observe a gentler terrain area with rolling hills and open fields. This region has a dry riverbed nearby surrounded by tall grasses and wildflowers. The terrain seems more manageable than the jungle or the rocky cliffs, presenting a potentially more accessible path for the adventurer to navigate.<br><br><em>Clue : \"Avast ye! Head towards the setting sun, beneath the shadow o' yonder mountain. Thar be a message o' the past carved into th' rock. Decipher it to know th' way ahead, me hearty!\"</em><br> Which direction you would choose : ", 'west'),
    ("As you reach the described location, you find yourself standing at the foot of a majestic mountain. The setting sun is casting an orange glow over the landscape, which is dotted with trees and rocks. At the base of the mountain, you see a large rock formation, which appears to have been carved into many years ago.<br><br>To the West: As you look towards the west, you see a vast expanse of desert. The sand stretches as far as your eyes can see, and the heat is intense. There appears to be no signs of life, and you get the sense that the journey in this direction may be arduous.<br><br>To the South: To the south, you see a dense forest. The trees are tall and thick, and the canopy above blocks out most of the sunlight. You can hear the sounds of wildlife emanating from within, and there is an air of mystery about the place.<br><br>To the North: Looking towards the north, you see a range of snowy mountains. The snow-capped peaks look both inviting and daunting. You can see many winding paths weaving up the mountains, and the possibility of adventure calls out to you.<br><br><em>Clue : \"Listen up, me hearties! Follow th' direction of th' Great Bear, where th' stars be shining brighter than pieces o' eight. Tread through th' thicket ahead and ye'll come across a path leadin' to th' unknown. Be brave, or be gone, ye filthy landlubbers!\"</em><br> Which direction you would choose : ", 'north'),
    ("As you reach the peak of the snowy mountain on the island, you see the landscape stretching out before you in all directions. The panoramic view is breath-taking, with the sparkling blue waters of the ocean spread out endlessly around the island with small patches of greenery and a few winding rivers.<br><br>To the East: Looking towards the east, you can see the edge of the island, where the ocean seems to stretch out endlessly. The water is calm and blue, presenting an almost ethereal atmosphere.<br><br>To the West: To the west, you can see the expanse of the island, with untouched forests, rivers, and mountains. The patchwork of green, snow, and rock creates a stunning vista, which visually appears almost untouchable, certainly unspoiled by human activity.<br><br>To the North: Looking towards the north, you see a range of hills that appear mostly covered with lush green forests. The crisp breeze carries with it the sounds of birds and other animals, indicating that this may be a path through the island's untouched wilderness.<br><br><em>Clue : \"Arrr, me hearties! Listen up! Where th' rivers and stones meet, be on the lookout for a secret path hidin' in plain sight. Follow the gentle wind's beat towards th' land o' unknown might. As th' sun rises, take th' road least traveled towards th' land o' midnight. Ascend through th' unraveled hills - and ye'll discover the answer to your plight. So weigh anchor and hoist the colors high - we've got a journey ahead, me trusty crew!\"</em><br> Which direction you would choose : " , 'north'),
    ("As you come to a stop after hours of searching, you find yourself on the edge of a hilltop, surrounded by lush green trees and bushes. The peaceful and serene atmosphere exudes a sense of tranquility that eases your mind.<br><br>To the North, you can see a few small huts of a local village with smoke rising from chimneys. The place seems to be bustling with activity, and you can hear faint sounds of people conversing and children playing.<br><br>To the East lies the vast expanse of the ocean stretching beyond the horizon, merging with the clear blue sky. You can feel the salty wind on your face and hear the sound of waves crashing against the rocks, creating a soothing melody.<br><br>To the West, you see a beautiful valley with a dense forest where the rustling of leaves and the chirping of birds add more charm to the scenic beauty. A small stream flows through the forest, providing a serene atmosphere.<br><br><em>Clue : \"Aye, me hearties! Listen up, for the clue ye seek lies at th' feet of an ancient goddess, whose face be hidden beneath a veil of grace. She guards the secrets o' th' west and only reveals them to those who stay true to their intentions. Seek her out where th' land meets th' sea, and ye shall behold your treasure. So hoist the Jolly Roger and prepare for a journey through unknown waters, me hearty!\"</em><br> Which direction you would choose : ", 'east'),
    ("As you reached the Godess Statue you see the following Words<br><br>\"Oh seeker of treasure, hearken to my words. Choose the path to your goal, knowing that the other paths will be forever lost. Which of the following paths will you take?<br><br> North: The path of wealth and power.<br><br>South: The path of knowledge and wisdom.<br><br>East: The path of love and compassion.<br><br>West: The path of adventure and thrill<br><br><br> Which direction you would choose : ", 'west')
]



# Variables to keep track of the current question and whether the treasure hunt has started
current_question = None
is_started = False
previous_answer = 'Enter'
start_time = time.time()
cur_user = None



@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        if 'username' in request.form:
            username = request.form['username']
        
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('signup.html', error='Username already taken')
        new_user = User(username=username,email = email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('sign_in'))
    else:
        return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    global cur_user
    if request.method == 'POST':
        username = None
        if 'username' in request.form:
            username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter_by(username=username, password=hashed_password).first()
        if user:
            session['username'] = username
            cur_user = username
            return redirect(url_for('treasure_hunt'))
        else:
            return render_template('signin.html', error='Invalid username or password')
    else:
        return render_template('signin.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        key = None
        if 'key' in request.form:
            key = request.form['key']

        if key == admin_makekey:
            username = None
            if 'username' in request.form:
                username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password != confirm_password:
                return render_template('admin.html', error='Passwords do not match')
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = User.query.filter_by(username=username).first()
            if user:
                return render_template('admin.html', error='Username already taken')
            new_user = Admin(adminname=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('admin_login'))
        else:
            return render_template('admin.html', error='Invalid Key')
    else:
        return render_template('admin.html')


@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = None
        if 'username' in request.form:
            username = request.form['username']

        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        admin = Admin.query.filter_by(adminname=username, password=hashed_password).first()

        if admin:
            session['username'] = username
            return redirect(url_for('view_users'))
        else:
            return render_template('adminlogin.html', error='Invalid username or password')
    else:
        return render_template('adminlogin.html')


@app.route('/logout', methods=[ 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('sign_in'))

@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/administrator')
def view_admins():
    admins = Admin.query.all()
    return render_template('admins.html', admins=admins)

@app.route('/reset')
def reset_db():
    db.drop_all()
    db.create_all()
    return 'Database reset successfully.'

# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def treasure_hunt():
    global current_question, is_started, previous_answer,start_time,cur_user

    if cur_user == None :
        #flash('ERROR : No User Login')
        return redirect(url_for('sign_in'))

    # If the treasure hunt has not started yet, render the start page
    if not is_started:
        if request.method == 'POST' and 'start' in request.form:
            # If the user clicks the start button, set is_started to True and render the first question
            is_started = True
            current_question = 0
            previous_answer = 'Enter Answer'
            start_time=time.time()
            return render_template('index.html', question=questions[current_question][0])
        else:
            # Otherwise, render the start page with the start button
            return render_template('start.html')

    # If the treasure hunt has started, render the current question
    else:
        if request.method == 'POST':
            # If the user submits an answer, check if it is correct and render the appropriate page
            if 'answer-input' in request.form:
                answer = request.form['answer-input']
                previous_answer = answer
            else:
                answer = previous_answer

            if answer.lower() == questions[current_question][1].lower():
                if current_question == len(questions) - 1:
                    # If this was the last question, render the success page and reset the treasure hunt
                    user = User.query.filter_by(username=cur_user).first()
                    # Check if the user exists
                    if user:
                        current_question = None
                        is_started = False
                        previous_answer = None
                        total_time = time.time() - start_time
                        if user.bstime > total_time :
                            user.bstime = total_time
                            db.session.commit()
                        return render_template('success.html',finish_time = total_time)
                    else:
                        # Handle the case where the user does not exist
                        flash('There was an error: No User Found' )
                        return redirect(url_for(sign_in))
                else:
                    # If there are more questions, move on to the next question
                    current_question += 1
                    previous_answer = None
                    return render_template('index.html', question=questions[current_question][0])
            else:
                # If the answer is incorrect, render the failure page
                return render_template('confirm.html')
        else:
            # If the user refreshes the page, show a dialog box to restart or continue
            return render_template('index.html', question=questions[current_question][0])

# Route for the restart button
@app.route('/restart', methods=['POST'])
def restart():
    global current_question, is_started, previous_answer,start_time
    current_question = None
    is_started = False
    previous_answer = None
    start_time = time.time()
    return render_template('start.html')




# # Route for continuing the treasure hunt
# @app.route('/continue', methods=['POST'])
# def continue_hunt():
#     global current_question
#     if 'question_num' in request.form:
#         current_question = int(request.form['question_num'])
#         return redirect(url_for('treasure_hunt'))
#     else:
#         global  is_started, previous_answer
#         current_question = None
#         is_started = False
#         previous_answer = None
#         return render_template('start.html')

if __name__ == '__main__':
    app.run(debug=True)

