import socket as sk
import AlphaBot
import threading
import time
import sqlite3
from flask import Flask, render_template,redirect, url_for, request
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)


#Address di connesione al robot
app = Flask(__name__)
app.secret_key = "DiddyEpstein69"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id


class DataCatcher(threading.Thread):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.value_l = 0
        self.value_r = 0
        self.running = True
        self.enable = True
    
    def run(self):
        while self.running:
            self.value_l = self.robot.readLeft()
            self.value_r = self.robot.readRight()
            if (self.value_r == 0 or self.value_l == 0) and self.enable:
                self.robot.stop()
            time.sleep(0.01)  # piccolo ritardo per non saturare la CPU

    def stop(self):
        self.running = False

#Classe di implementazione controlli personalizzati
class Control():
    def __init__(self, left, right, robot):
        self.left = left
        self.right = right
        self.robot = robot
        self.letter = ''
        
    def setSpeed(self,msg):
        if msg in speeds:
            self.left = speeds[msg]
            self.right = speeds[msg]

    def modularFw(self):
        self.robot.setMotor(self.left,-self.right)
        
    def modularBw(self):
        self.robot.setMotor(-self.left,self.right)

#Istanziamento classe   
Ab = AlphaBot.AlphaBot()
dataCatch = DataCatcher(Ab)
ctrl = Control(40, 40, Ab)
dataCatch.start()
    
#dizionario di controllo del robot
#in base al carattere ricevuto viene chiamata la rispettiva funzione
movemnts = {
    "Ab.forward()": Ab.forward,
    "Ab.backward()": Ab.backward,
    "Ab.left()": Ab.left,
    "Ab.right()": Ab.right,
    "Ab.ex()": Ab.ex,
    "Ab.stop()": Ab.stop,
    "ctrl.modularFw()": ctrl.modularFw,
    "ctrl.modularBw()": ctrl.modularBw,
    "Ab.square()": Ab.square,
    "Ab.circle()": Ab.circle
}

#dizionario di controllo per le velocità
speeds = {
    "1": 33,
    "2": 70,
    "3": 100
}


def web_server():
    conn = sqlite3.connect('../db/db_controllo_alfabot.db')
    cur = conn.cursor()
    ctrl.setSpeed(ctrl.letter)
    if ctrl.letter== "s":
        dataCatch.enable = False
    if ctrl.letter== "w":
        dataCatch.enable = True
    print(ctrl.letter)
    cur.execute(f"SELECT function FROM controlli WHERE control_char = '{ctrl.letter}'")
    command = cur.fetchall()[0][0]
    movemnts[command]()
    conn.close()

# @login_manager.user_loader
# def load_user(user_id):
#     if user_id in USERS:
#         return User(user_id)
#     return None

@app.route("/login", methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('../db/users.db')
    cur = conn.cursor()
    if request.method == 'POST':
        pswd = request.form.get("password")
        username = request.form.get("nome")
        cur.execute(f"SELECT users.username, users.password FROM users WHERE users.username = {username}")
        data = cur.fetchall()
        print(data)
    conn.close()
    return render_template('login.html')

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Prendi i valori dal form
        ctrl.letter = request.form.get('lettera')
        print(f"Lettera ricevuta: {ctrl.letter}")
        web_server()
    return render_template('index.html')
    
app.run(host="0.0.0.0", port = "6767", debug=False)

Ab.stop()
  
               