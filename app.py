import numpy as np
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from datetime import timedelta
import os
import pandas as pd
from wtforms import SelectField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired , Email, Length
from flask_wtf import FlaskForm
import pulp
import sys
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from models import db, users6
from lookup import myDict 
from Pulp_optimization import Pulp_optimization
from datafile import Data, Data_ECS, Data_EG, Data_EW, N, Names, Teams,Value,Positions,xPoints,xPoints2, xPoints3,xPoints4, xPoints5,xPoints6, xPointsTotal, TotalPoints, Transfer, Cost, xGrowth,Names, TotalPoints, Cost, Positions,Teams, xPoints, Transfer 
# USe env\Scripts\Activate.ps1 to activate venv
# os.chdir('C:/Users/hk1maso/Footballpage')

app = Flask(__name__,template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Stor6612@localhost:5432/flask"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://pnbgdrhhgszifs:ccee2ed3aa53813ba15a0810d7d2f0ffb324c06a3b56f13d0c87571aca463791@ec2-54-146-73-98.compute-1.amazonaws.com:5432/d5h5t687jv1hvq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hello"

db.init_app(app)
migrate = Migrate(app, db)

Bootstrap(app)

ExcludePlayers = [] 
IncludePlayers = [] 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(found_user_id):
    return users6.query.get(int(found_user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
        

class Form(FlaskForm):
    Budget = StringField('Budget', validators=[Length(max=50),InputRequired()])
    Player1 = SelectField('Player1',choices=[])
    Player2 = SelectField('Player2',choices=[])
    Player3 = SelectField('Player3',choices=[])
    Player4 = SelectField('Player4',choices=[])    
    Player5 = SelectField('Player5',choices=[])
    Player6 = SelectField('Player6',choices=[])
    Player7 = SelectField('Player7',choices=[])
    Player8 = SelectField('Player8',choices=[])
    Player9 = SelectField('Player9',choices=[])
    Player10 = SelectField('Player10',choices=[])
    Player11 = SelectField('Player11',choices=[])
    Player1EX = SelectField('Player1EX',choices=[])
    Player2EX = SelectField('Player2EX',choices=[])
    Player3EX = SelectField('Player3EX',choices=[])
    Player4EX = SelectField('Player4EX',choices=[])    
    Player5EX = SelectField('Player5EX',choices=[])
    Player1IN = SelectField('Player1IN',choices=[])
    Player2IN = SelectField('Player2IN',choices=[])
    Player3IN = SelectField('Player3IN',choices=[])
    Player4IN = SelectField('Player4IN',choices=[])    
    Player5IN = SelectField('Player5IN',choices=[])
    Team1EX = SelectField('Team1EX',choices=[])
    Team2EX = SelectField('Team2EX',choices=[])
    Team3EX = SelectField('Team3EX',choices=[])
    Team4EX = SelectField('Team4EX',choices=[])    
    Team5EX = SelectField('Team5EX',choices=[])

choices = [("Please Select")]

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/Viewlist/')
def Viewlist():
     
    username = session["user"]
    found_user = users6.query.filter_by(username=username).first()
      
    if found_user.Player1:
        print("""non empty""")
        form = Form()
        print(found_user.Budget)
        form.Budget.data = found_user.Budget
        form.Player1.choices = [(found_user.Player1),"---"]+sorted(Names)
        form.Player2.choices = [(found_user.Player2),"---"]+sorted(Names)
        form.Player3.choices = [(found_user.Player3),"---"]+sorted(Names)
        form.Player4.choices = [(found_user.Player4),"---"]+sorted(Names)
        form.Player5.choices = [(found_user.Player5),"---"]+sorted(Names)
        form.Player6.choices = [(found_user.Player6),"---"]+sorted(Names)
        form.Player7.choices = [(found_user.Player7),"---"]+sorted(Names)
        form.Player8.choices = [(found_user.Player8),"---"]+sorted(Names)
        form.Player9.choices = [(found_user.Player9),"---"]+sorted(Names)
        form.Player10.choices = [(found_user.Player10),"---"]+sorted(Names)
        form.Player11.choices = [(found_user.Player11),"---"]+sorted(Names)
    
    else:
        print("""empty""")
        form = Form()
        form.Player1.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player2.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player3.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player4.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player5.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player6.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player7.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player8.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player9.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player10.choices = [('Please Select'),"---"]+sorted(Names)
        form.Player11.choices = [('Please Select'),"---"]+sorted(Names)
             
    return render_template("ViewList.html", form=form)

@app.route("/login/",methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        
        found_user = users6.query.filter_by(username=form.username.data).first()
        
        if found_user:
            if check_password_hash(found_user.password, form.password.data):
                session.permanent = True
                session["user"] = form.username.data
                
                login_user(found_user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
                
        return '<h1>Invalid username or password</h1>'
   
    return render_template("login.html", form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = users6(username=form.username.data, email=form.email.data, password=hashed_password,
                         Budget=0, Player1 = '',Player2 = '', Player3 = '', Player4 = '', Player5 = '', Player6 = '',
                         Player7 = '',Player8 = '', Player9 = '', Player10 = '', Player11 = '')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('signup.html', form=form)

@app.route("/optimization",methods=["POST","GET"])
def optimization():
    if request.method == 'POST':
    
        username = session["user"]
        found_user = users6.query.filter_by(username=username).first()
        Budget = found_user.Budget
        Player1 = found_user.Player1
        Player2 = found_user.Player2
        Player3 = found_user.Player3
        Player4 = found_user.Player4
        Player5 = found_user.Player5
        Player6 = found_user.Player6
        Player7 = found_user.Player7
        Player8 = found_user.Player8
        Player9 = found_user.Player9
        Player10 = found_user.Player10
        Player11 = found_user.Player11
        
        PlayerList = list([Player1,Player2,Player3,Player4,Player5,Player6,Player7,Player8,Player9,Player10,Player11])
        
        del Player1,Player2,Player3,Player4,Player5,Player6,Player7,Player8,Player9,Player10,Player11
                  
        Player1EX = request.form.get("Player1EX")
        Player2EX = request.form.get("Player2EX")
        Player3EX = request.form.get("Player3EX")
        Player4EX = request.form.get("Player4EX")
        Player5EX = request.form.get("Player5EX")
        ExcludePlayers = [Player1EX, Player2EX, Player3EX, Player4EX, Player5EX] 
        
        del Player1EX, Player2EX, Player3EX, Player4EX, Player5EX
        Player1IN = request.form.get("Player1IN")
        Player2IN = request.form.get("Player2IN")
        Player3IN = request.form.get("Player3IN")
        Player4IN = request.form.get("Player4IN")
        Player5IN = request.form.get("Player5IN")  
        
        IncludePlayers = [Player1IN, Player2IN, Player3IN, Player4IN, Player5IN] 
        del Player1IN, Player2IN, Player3IN, Player4IN, Player5IN
        
        Team1EX = request.form.get('Team1EX')
        Team2EX = request.form.get('Team2EX')
        Team3EX = request.form.get('Team3EX')
        Team4EX = request.form.get('Team4EX')    
        Team5EX = request.form.get('Team5EX')
        ExcludeTeam = [Team1EX, Team2EX, Team3EX, Team4EX, Team5EX] 
        
        del Team1EX, Team2EX, Team3EX, Team4EX, Team5EX
        
        Squad, Squad_Team, Squad_xPoints, Squad_Position, Squad_Captain, Budget, TransferCost, nShare, Expected_points = Pulp_optimization(Teams, N, Data, Value, PlayerList,xPointsTotal, 
                                                             Positions, ExcludePlayers, IncludePlayers, ExcludeTeam,1,Budget, Names, xPoints)
        
        if Squad != 0:

            if 'Please Select' in ExcludePlayers:
                ExcludePlayers = (value for value in ExcludePlayers if value != 'Please Select')
            if 'Please Select' in ExcludeTeam:
                ExcludeTeam = (value for value in ExcludeTeam if value != 'Please Select')   
            
            print(nShare)
            return render_template("Dashboard2.html", Squad = Squad, Squad_Position = Squad_Position ,Squad_Team = Squad_Team, 
                                                        Squad_xPoints = Squad_xPoints, ExcludePlayers  = ExcludePlayers, ExcludeTeam = ExcludeTeam,
                                                        Squad_Captain = Squad_Captain, Budget = Budget, TransferCost = TransferCost, 
                                                        nShare = nShare, Expected_points = Expected_points)   
        else:
            error_statement = "Something went wrong with the optimization, please check your team and budget and edit if needed"
            Squad=['Edit your team']
            Squad_Position = ['']
            Squad_Team = ['']
            Squad_xPoints = ['']
            Squad_Captain = ['']
            labels = 7 * ['']
            values = 7 * [0]
            nShare = 0
            Budget = 0
            TransferCost = 0
            Expected_points = 0
            return render_template('fail.html', name=current_user.username, Squad = Squad, Squad_Position = Squad_Position ,Squad_Team = Squad_Team, 
                                            Squad_xPoints = Squad_xPoints, Squad_Captain = Squad_Captain, labels=labels, values=values,
                                            nShare = nShare, Budget = Budget,error_statement=error_statement
                                            )
    else:
        
        return redirect(url_for('teamselected'))
    
@app.route("/teamupdated", methods=["POST"])
def teamupdated():
    
    Squad = request.form.getlist("Name")
    
    username = session["user"]
    found_user = users6.query.filter_by(username=username).first()
    
    found_user.Player1 = Squad[0]
    found_user.Player2 = Squad[1]
    found_user.Player3 = Squad[2]
    found_user.Player4 = Squad[3]
    found_user.Player5 = Squad[4]
    found_user.Player6 = Squad[5]
    found_user.Player7 = Squad[6]
    found_user.Player8 = Squad[7]
    found_user.Player9 = Squad[8]
    found_user.Player10 = Squad[9]
    found_user.Player11 = Squad[10]
    db.session.commit()    
    
    return redirect(url_for('dashboard'))

@app.route("/Adjustoptimization", methods=["POST"])
def sure():
    if request.method == 'POST':    
        print(request.form.getlist("mycheckbox"))
        print(request.form.getlist("Name"))
        print(request.form.getlist("mycheckboxExcludePLayer"))
        print(request.form.getlist("ExcludedPlayers"))
        print(request.form.getlist("mycheckboxExcludedTeams"))
        print(request.form.getlist("ExcludedTeams"))
        
        included = request.form.getlist("mycheckbox")
        suggested_players = request.form.getlist("Name")
        excludedP = request.form.getlist("mycheckboxExcludePLayer")
        excludedPlayers = request.form.getlist("ExcludedPlayers")
        excludedT = request.form.getlist("mycheckboxExcludedTeams")
        excludedTeams = request.form.getlist("ExcludedTeams")
        
        ExcludePlayers=[]
        IncludePlayers=[]
        ExcludeTeam=[]
        
        for i in range(len(suggested_players)):
            if str(i+1) in included:
                ExcludePlayers.append(suggested_players[i]) 
            else:
                IncludePlayers.append(suggested_players[i]) 
                
        print(range(len(excludedPlayers)))    
        for i in range(len(excludedPlayers)):
            if str(i+1) in excludedP:
                ExcludePlayers.append(excludedPlayers[i]) 
                print(ExcludePlayers)
        
        print(range(len(excludedTeams)))  
        for i in range(len(excludedTeams)):
            if str(i+1) in excludedT:
                ExcludeTeam.append(excludedTeams[i]) 
        
        print(ExcludePlayers)
        print(IncludePlayers)
        print(ExcludeTeam)
        
        username = session["user"]
        found_user = users6.query.filter_by(username=username).first()
        Budget = found_user.Budget
        Player1 = found_user.Player1
        Player2 = found_user.Player2
        Player3 = found_user.Player3
        Player4 = found_user.Player4
        Player5 = found_user.Player5
        Player6 = found_user.Player6
        Player7 = found_user.Player7
        Player8 = found_user.Player8
        Player9 = found_user.Player9
        Player10 = found_user.Player10
        Player11 = found_user.Player11
        
        PlayerList = list([Player1,Player2,Player3,Player4,Player5,Player6,Player7,Player8,Player9,Player10,Player11])
        
        print(PlayerList)

        Squad, Squad_Team, Squad_xPoints, Squad_Position, Squad_Captain, Budget, TransferCost, nShare, Expected_points = Pulp_optimization(Teams, N, Data, Value, PlayerList,xPointsTotal, 
                                                         Positions, ExcludePlayers, IncludePlayers, ExcludeTeam,2, Budget, Names, xPoints)
        
        print(ExcludePlayers)
        print(IncludePlayers)
        print(ExcludeTeam)
        
        
        
        return render_template("Dashboard2.html", Squad = Squad, Squad_Position = Squad_Position ,Squad_Team = Squad_Team, 
                                                    Squad_xPoints = Squad_xPoints, ExcludePlayers  = ExcludePlayers, ExcludeTeam = ExcludeTeam,
                                                    Squad_Captain = Squad_Captain, Budget = Budget, TransferCost = TransferCost, 
                                                    nShare = nShare, Expected_points = Expected_points)   

    
@app.route("/teamselected",methods=["POST","GET"])
def teamselected():
    
    if request.method == "POST":
        Budget = request.form.get("Budget")
        Player1 = request.form.get("Player1")
        Player2 = request.form.get("Player2")
        Player3 = request.form.get("Player3")
        Player4 = request.form.get("Player4")
        Player5 = request.form.get("Player5")
        Player6 = request.form.get("Player6")
        Player7 = request.form.get("Player7")
        Player8 = request.form.get("Player8")
        Player9 = request.form.get("Player9")
        Player10 = request.form.get("Player10")
        Player11 = request.form.get("Player11")
        
        PlayerList = [Player1,Player2,Player3,Player4,Player5,Player6,Player7,Player8,Player9,Player10,Player11]
        
        username = session["user"]
        found_user = users6.query.filter_by(username=username).first()
        found_user.Budget = Budget
        found_user.Player1 = Player1
        found_user.Player2 = Player2
        found_user.Player3 = Player3
        found_user.Player4 = Player4
        found_user.Player5 = Player5
        found_user.Player6 = Player6
        found_user.Player7 = Player7
        found_user.Player8 = Player8
        found_user.Player9 = Player9
        found_user.Player10 = Player10
        found_user.Player11 = Player11
        db.session.commit()    
      
    form = Form()
    form.Player1EX.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player2EX.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player3EX.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player4EX.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player5EX.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player1IN.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player2IN.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player3IN.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player4IN.choices = [('Please Select'),"---"]+sorted(Names)
    form.Player5IN.choices = [('Please Select'),"---"]+sorted(Names)
    form.Team1EX.choices = [('Please Select'),"---"]+sorted(list(set(sorted(Teams))))
    form.Team2EX.choices = [('Please Select'),"---"]+sorted(list(set(sorted(Teams))))
    form.Team3EX.choices = [('Please Select'),"---"]+sorted(list(set(sorted(Teams))))
    form.Team4EX.choices = [('Please Select'),"---"]+sorted(list(set(sorted(Teams))))
    form.Team5EX.choices = [('Please Select'),"---"]+sorted(list(set(sorted(Teams))))
    
    
    return render_template("teamselected.html",  form=form)

@app.route('/dashboard2')
def dashboard2():
    return render_template('dashboard2.html')
    
@app.route('/dashboard')
@login_required
def dashboard():
    username = session["user"]
    found_user = users6.query.filter_by(username=username).first()
    print(found_user.Player1)
    
    if found_user.Player11!='':
        Squad=[]   
        Budget = found_user.Budget
        Squad.append(found_user.Player1)
        Squad.append(found_user.Player2)
        Squad.append(found_user.Player3)
        Squad.append(found_user.Player4)
        Squad.append(found_user.Player5)
        Squad.append(found_user.Player6)
        Squad.append(found_user.Player7)
        Squad.append(found_user.Player8)
        Squad.append(found_user.Player9)
        Squad.append(found_user.Player10)
        Squad.append(found_user.Player11)
   
        Squad, Squad_Team, Squad_xPoints, Squad_Position, Squad_Captain, Budget, TransferCost, nShare, Expected_points = Pulp_optimization(Teams, N, Data, Value, Squad, xPointsTotal, 
                                                                                            Positions, [], Squad, [], 0, Budget, Names, xPoints)
        if Squad != 0:
            index = np.where(np.in1d(Names, Squad))[0] 
            Team_help = [Teams[i] for i in index]
            Labels, Values = np.unique(Team_help, return_counts=True)
            labels = 7 * [None]
            values = 7 * [None]
            
            print(len(Labels))
            for i in range(len(Labels)):
                labels[i] = myDict[Labels[i].tolist()]
                values[i] = Values[i].tolist()
            
        else:
            error_statement = "Something went wrong with the optimization, please check your team and budget and edit if needed"
            Squad=['Edit your team']
            Squad_Position = ['']
            Squad_Team = ['']
            Squad_xPoints = ['']
            Squad_Captain = ['']
            labels = 7 * ['']
            values = 7 * [0]
            nShare = 0
            Budget = 0
            TransferCost = 0
            Expected_points = 0
            return render_template('fail.html', name=current_user.username, Squad = Squad, Squad_Position = Squad_Position ,Squad_Team = Squad_Team, 
                                            Squad_xPoints = Squad_xPoints, Squad_Captain = Squad_Captain, labels=labels, values=values,
                                            nShare = nShare, Budget = Budget,error_statement=error_statement
                                            )

    else:
        Squad=['No team yet, edit your team']
        Squad_Position = ['']
        Squad_Team = ['']
        Squad_xPoints = ['']
        Squad_Captain = ['']
        labels = 7 * ['']
        values = 7 * [0]
        nShare = 0
        Budget = 0
        TransferCost = 0
        Expected_points = 0

    return render_template('dashboard.html', name=current_user.username, Squad = Squad, Squad_Position = Squad_Position ,Squad_Team = Squad_Team, 
                                               Squad_xPoints = Squad_xPoints, Squad_Captain = Squad_Captain, labels=labels, values=values,
                                               nShare = nShare, Budget = Budget
                                               )

@app.route('/top100')
@login_required
def top100():
 
    username = session["user"]
    found_user = users6.query.filter_by(username=username).first()
    
    if found_user.Player1!='':
        Squad=[]   
        Budget = found_user.Budget
        Squad.append(found_user.Player1)
        Squad.append(found_user.Player2)
        Squad.append(found_user.Player3)
        Squad.append(found_user.Player4)
        Squad.append(found_user.Player5)
        Squad.append(found_user.Player6)
        Squad.append(found_user.Player7)
        Squad.append(found_user.Player8)
        Squad.append(found_user.Player9)
        Squad.append(found_user.Player10)
        Squad.append(found_user.Player11)
   
        Squad, Squad_Team, Squad_xPoints, Squad_Position, Squad_Captain, Budget, TransferCost, nShare, Expected_points = Pulp_optimization(Teams, N, Data, Value, Squad, xPointsTotal, 
                                                                                            Positions, [], Squad, [], 0, Budget, Names, xPoints)
        
        Transfer = list(np.where(np.isin(list(Data['Name']), Squad),0,np.array(Value)*0.01)) #Value*0,01 if on team    
    else:
        Transfer = list(np.where(np.isin(list(Data['Name']), ''),0,0)) #Value*0,01 if on team    

    
    xPointsTotal1 = list(Data['xPoints Total']) #X points total
    TotalPoints = list(np.array(xPointsTotal1)  - np.array(Transfer))        
    xGrowth = list(np.array(TotalPoints)/np.array(Value))
    indices =  sorted(range(len(TotalPoints)), key = lambda sub: TotalPoints[sub])[-100:]
    indices = list(reversed(np.array(indices)))
    
    TotPoints = [round(TotalPoints[i],0) for i in indices]
    Name = [Names[i] for i in indices]
    Team1 = [Teams[i] for i in indices]
    xPoints1 = [round(xPoints[i],0) for i in indices]
    xPointsTotal1 = [round(xPointsTotal[i],0) for i in indices]
    Transfer1 = [round(Transfer[i],0) for i in indices]
    TotalPoints1  = [round(TotalPoints[i],0) for i in indices] 
    xGrowth1  = [round(xGrowth[i],2)*100 for i in indices]   
    
    return render_template('top100.html', TotPoints=TotPoints, Name = Name, Team1 = Team1 ,xPoints1 = xPoints1, Transfer1 = Transfer1,
                                           xPointsTotal1 = xPointsTotal1, TotalPoints1 = TotalPoints1, xGrowth1=xGrowth1)

@app.route('/top100growth')
@login_required
def top100growth():
 
    username = session["user"]
    found_user = users6.query.filter_by(username=username).first()
    print(username)
    
    if found_user.Player1!='':
        Squad=[]   
        Budget = found_user.Budget
        Squad.append(found_user.Player1)
        Squad.append(found_user.Player2)
        Squad.append(found_user.Player3)
        Squad.append(found_user.Player4)
        Squad.append(found_user.Player5)
        Squad.append(found_user.Player6)
        Squad.append(found_user.Player7)
        Squad.append(found_user.Player8)
        Squad.append(found_user.Player9)
        Squad.append(found_user.Player10)
        Squad.append(found_user.Player11)
   
        Squad, Squad_Team, Squad_xPoints, Squad_Position, Squad_Captain, Budget, TransferCost, nShare, Expected_points = Pulp_optimization(Teams, N, Data, Value, Squad, xPointsTotal, 
                                                                                            Positions, [], Squad, [], 0, Budget, Names, xPoints)
        
        Transfer = list(np.where(np.isin(list(Data['Name']), Squad),0,np.array(Value)*0.01)) #Value*0,01 if on team    
    else:
        Transfer = list(np.where(np.isin(list(Data['Name']), ''),0,0)) #Value*0,01 if on team    

    
    xPointsTotal1 = list(Data['xPoints Total']) #X points total
    TotalPoints = list(np.array(xPointsTotal1)  - np.array(Transfer))        
    xGrowth = list(np.array(TotalPoints)/np.array(Value))
    indices =  sorted(range(len(xGrowth)), key = lambda sub: xGrowth[sub])[-100:]
    indices = list(reversed(np.array(indices)))
    
    TotPoints = [round(TotalPoints[i],0) for i in indices]
    Name = [Names[i] for i in indices]
    Team1 = [Teams[i] for i in indices]
    xPoints1 = [round(xPoints[i],0) for i in indices]
    xPointsTotal1 = [round(xPointsTotal[i],0) for i in indices]
    Transfer1 = [round(Transfer[i],0) for i in indices]
    TotalPoints1  = [round(TotalPoints[i],0) for i in indices] 
    xGrowth1  = [round(xGrowth[i],2)*100 for i in indices]   
    
    return render_template('top100growth.html', TotPoints=TotPoints, Name = Name, Team1 = Team1 ,xPoints1 = xPoints1, Transfer1 = Transfer1,
                                           xPointsTotal1 = xPointsTotal1, TotalPoints1 = TotalPoints1, xGrowth1=xGrowth1)

@app.route('/ExpectedCS', methods=['GET', 'POST'])
@login_required
def ExpectedCS():
    
    Team1 = list(Data_ECS['Team'])
    col1 = list(round(Data_ECS[1],2))
    col2 = list(round(Data_ECS[2],2))
    col3 = list(round(Data_ECS[3],2))
    col4 = list(round(Data_ECS[4],2))
    col5 = list(round(Data_ECS[5],2))
    col6 = list(round(Data_ECS[6],2))  
    Avg = list(round(Data_ECS['Avg'],2))
    Min = list(round(Data_ECS['Min'],2))
    Max = list(round(Data_ECS['Max'],2))  

    return render_template('ExpectedCS.html', Team1=Team1, col1=col1, col2=col2, col3=col3, 
                                                col4=col4, col5=col5, col6=col6, Avg=Avg,Min=Min, Max=Max)
                           
@app.route('/ExpectedG', methods=['GET', 'POST'])
@login_required
def ExpectedG():
    
    Team1 = list(Data_EG['Team'])
    col1 = list(round(Data_EG[1],2))
    col2 = list(round(Data_EG[2],2))
    col3 = list(round(Data_EG[3],2))
    col4 = list(round(Data_EG[4],2))
    col5 = list(round(Data_EG[5],2))
    col6 = list(round(Data_EG[6],2))  
    Avg = list(round(Data_EG['Avg'],2))
    Min = list(round(Data_EG['Min'],2))
    Max = list(round(Data_EG['Max'],2))  

    return render_template('ExpectedG.html', Team1=Team1, col1=col1, col2=col2, col3=col3, 
                                                col4=col4, col5=col5, col6=col6, Avg=Avg,Min=Min, Max=Max)

@app.route('/ExpectedW', methods=['GET', 'POST'])
@login_required
def ExpectedW():
    
    Team1 = list(Data_ECS['Team'])
    col1 = list(round(Data_EW[1],2))
    col2 = list(round(Data_EW[2],2))
    col3 = list(round(Data_EW[3],2))
    col4 = list(round(Data_EW[4],2))
    col5 = list(round(Data_EW[5],2))
    col6 = list(round(Data_EW[6],2))  
    Avg = list(round(Data_EW['Avg'],2))
    Min = list(round(Data_EW['Min'],2))
    Max = list(round(Data_EW['Max'],2))  

    return render_template('ExpectedW.html', Team1=Team1, col1=col1, col2=col2, col3=col3, 
                                                col4=col4, col5=col5, col6=col6, Avg=Avg,Min=Min, Max=Max)
                           
@app.route('/AnalyzePlayers', methods=['GET', 'POST'])
@login_required
def AnalyzePlayers():
    
    print(request.method)
    if request.method =='GET':
        
        username = session["user"]
        found_user = users6.query.filter_by(username=username).first()
        
        if found_user.Player1!='':
            Player1_index = Names.index(found_user.Player1)
            Player2_index = Names.index(found_user.Player2)
        else:
            Player1_index = 1
            Player2_index = 2
    else:
        Player1_index = Names.index(request.form.get("Player1"))
        Player2_index = Names.index(request.form.get("Player2"))        
        print(request.form.get("Player2"))
        print(request.form.get("Player1"))
        
    form = Form()
    form.Player1.choices = [("Please Select"),"---"]+sorted(Names)
    form.Player2.choices = [("Please Select"),"---"]+sorted(Names)
    
    labels = ['1','2','3','4','5','6']
    values1 = [xPoints[Player1_index],xPoints2[Player1_index],xPoints3[Player1_index],
               xPoints4[Player1_index],xPoints5[Player1_index],xPoints6[Player1_index]]
    
    values2 = [xPoints[Player2_index],xPoints2[Player2_index],xPoints3[Player2_index],
               xPoints4[Player2_index],xPoints5[Player2_index],xPoints6[Player2_index]]

    average = [np.mean(np.array(xPoints)[np.array(xPoints)>0]).tolist(),
               np.mean(np.array(xPoints2)[np.array(xPoints2)>0]).tolist(),
               np.mean(np.array(xPoints3)[np.array(xPoints3)>0]).tolist(),
               np.mean(np.array(xPoints4)[np.array(xPoints4)>0]).tolist(),
               np.mean(np.array(xPoints5)[np.array(xPoints5)>0]).tolist(),
               np.mean(np.array(xPoints6)[np.array(xPoints6)>0]).tolist()]
    
    Name1 = Names[Player1_index]
    Name2 = Names[Player2_index]
    
    print(Name1)
    
    print(Name2)
    return render_template('AnalyzePlayers.html', labels=labels, values1=values1,values2=values2, 
                                                  form=form, average=average, Name1=Name1, Name2=Name2)

  
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/Aboutus')
@login_required
def Aboutus():
    return render_template('Aboutus.html')

@app.route('/FAQ')
@login_required
def FAQ():
    return render_template('FAQ.html')

@app.route('/Authors')
@login_required
def Authors():
    return render_template('Authors.html')

@app.route('/Howitworks')
@login_required
def Howitworks():
    return render_template('Howitworks.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, use_reloader=False)