import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iotproject'

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Define user file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
USER_FILE = os.path.join(BASE_DIR, "users.txt")  # Ensure users.txt is in the same folder

# Function to save a new user to users.txt
def save_user(username, email, password):
    with open(USER_FILE, "a") as file:  # Open in append mode
        file.write(f"{username}, {email}, {password}\n")

# Function to load users from the file into a dictionary
def load_users():
    users = {}
    if os.path.exists(USER_FILE):  # Ensure the file exists
        with open(USER_FILE, "r") as file:
            for line in file:
                try:
                    username, email, password = line.strip().split(", ")
                    users[username] = password  # Store username-password in dictionary
                except ValueError:
                    continue  # Skip malformed lines
    return users

# Load users into memory
users = load_users()

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:  # Check if user exists
        return User(user_id)
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Ensure passwords match
        if password != confirm_password:
            return "Passwords do not match, please try again."

        # Reload users to check if username is taken
        global users
        users = load_users()

        if username in users:
            return "Username already exists, please choose another one."

        # Save new user to file
        save_user(username, email, password)

        # Reload users after adding a new one
        users = load_users()

        return redirect(url_for("login"))  # Redirect to login page after registration

    return render_template('auth/register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Reload users before login attempt
        global users
        users = load_users()

        if username in users and users[username] == password:
            user = User(username)
            login_user(user)  # Log in the user
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password. Please try again."

    return render_template('auth/login.html', error=error)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/building1')
@login_required
def building1():
    return render_template("building/building1.html")

@app.route('/building2')
@login_required
def building2():
    return render_template("building/building2.html")


@app.route('/room1')
@login_required
def room1():
    return render_template("rooms/room1.html")

@app.route('/room2')
@login_required
def room2():
    return render_template("rooms/room2.html")


@app.route('/room3')
@login_required
def room3():
    return render_template("rooms/room3.html")

@app.route('/room4')
@login_required
def room4():
    return render_template("rooms/room4.html")
if __name__ == '__main__':
    app.run(debug=True)
