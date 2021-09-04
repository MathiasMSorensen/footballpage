from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
 
class users11(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(250))
    email = db.Column(db.String(100))
    Budget = db.Column(db.Integer())
    Player1 = db.Column(db.String(50))
    Player2 = db.Column(db.String(50))
    Player3 = db.Column(db.String(50))
    Player4 = db.Column(db.String(50))
    Player5 = db.Column(db.String(50))
    Player6 = db.Column(db.String(50))
    Player7 = db.Column(db.String(50))
    Player8 = db.Column(db.String(50))
    Player9 = db.Column(db.String(50))
    Player10 = db.Column(db.String(50))
    Player11 = db.Column(db.String(50))
    Player12 = db.Column(db.String(50))
    Player13 = db.Column(db.String(50))
    Player14 = db.Column(db.String(50))
    Player15 = db.Column(db.String(50))

    def __init__(self, username, password, email, Budget, Player1, Player2, Player3, \
                 Player4, Player5, Player6, Player7, Player8, Player9, Player10, Player11, \
                 Player12, Player13, Player14, Player15):

        self.username = username
        self.email = email
        self.password = password
        self.Budget = Budget
        self.Player1 = Player1
        self.Player2 = Player2
        self.Player3 = Player3
        self.Player4 = Player4
        self.Player5 = Player5
        self.Player6 = Player6
        self.Player7 = Player7
        self.Player8 = Player8
        self.Player9 = Player9
        self.Player10 = Player10
        self.Player11 = Player11
        self.Player11 = Player12
        self.Player11 = Player13
        self.Player11 = Player14
        self.Player11 = Player15
