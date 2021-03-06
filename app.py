import numpy as np
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from datetime import timedelta
import os
import pandas as pd
from pandas.core.frame import DataFrame
from wtforms import SelectField, StringField, PasswordField, BooleanField, IntegerField, validators
from wtforms.validators import InputRequired , Email, Length, NumberRange
from flask_wtf import FlaskForm
import pulp
import sys
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from models import db, users11
from lookup import myDict 
from Pulp_optimization import Pulp_optimization
from datetime import datetime, timedelta
from player_predictions import data_final, N, fte_to_web_xg, fte_to_web_xw ,fte_to_web_cs, Player_stats
from assumptions import current_round , forecast_window , discount_factor , sub_1_discount , sub_2_discount , sub_3_discount ,sub_gk_discount ,cash, date, n_transfer
from dictionaries import team_lookup_reverse, dict_players_rev, team_lookup, dict_players, team_lookup_num, team_lookup_num_reverse, position_lookup
from utils import get_optim_results, get_current_team

# from datafile import Data, Names2, Data_ECS, Data_EG, Data_EW, N, Names, Teams,Value,Positions,xPoints,xPoints2, xPoints3,xPoints4, xPoints5,xPoints6, xPointsTotal, TotalPoints, Transfer, Cost, xGrowth,Names, TotalPoints, Cost, Positions,Teams, xPoints, Transfer 
# USe env\Scripts\Activate.ps1 to activate venv
# os.chdir('C:/Users/hk1maso/Footballpage')

app = Flask(__name__,template_folder="templates")

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Stor6612@localhost:5432/flask"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://pnbgdrhhgszifs:ccee2ed3aa53813ba15a0810d7d2f0ffb324c06a3b56f13d0c87571aca463791@ec2-54-146-73-98.compute-1.amazonaws.com:5432/d5h5t687jv1hvq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hello"

db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)

Bootstrap(app)

ExcludePlayers = [] 
IncludePlayers = [] 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(found_user_id):
    return users11.query.get(int(found_user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=40)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
        
class Form(FlaskForm):
    Budget = IntegerField('How Many?', validators=[NumberRange(min=0, max=150, message='bla')])
    n_tranfers = SelectField('How Many?', validators=[NumberRange(min=1, max=2, message='bla')])
    Cost1 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost2 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost3 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost4 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost5 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost6 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost7 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost8 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost9 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost10 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost11 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost12 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost13 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost14 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    Cost15 = IntegerField('How Many?', validators=[NumberRange(min=3, max=15, message='bla')])
    
    Player1 = SelectField('Player1',choices=[], validators=[InputRequired()])
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
    Player12 = SelectField('Player12',choices=[])
    Player13 = SelectField('Player13',choices=[])
    Player14 = SelectField('Player14',choices=[])
    Player15 = SelectField('Player15',choices=[])
    Team1EX = SelectField('Team1EX',choices=[])
    Team2EX = SelectField('Team2EX',choices=[])
    Team3EX = SelectField('Team3EX',choices=[])
    Team4EX = SelectField('Team4EX',choices=[])    
    Team5EX = SelectField('Team5EX',choices=[])
    Player1IN = SelectField('Player1',choices=[])
    Player2IN = SelectField('Player2',choices=[])
    Player3IN = SelectField('Player3',choices=[])

choices = [("Please Select")]

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/Viewlist3/',methods=["POST","GET"])
def Viewlist3():

    fpl_name = data_final['fpl_name'] 
    fpl_cost = data_final[['fpl_name','cost']] 
    username = session["user"]
    found_user = users11.query.filter_by(username=username).first()
    form = Form()
    if request.method == 'POST': 
        Budget = request.form.get("Budget").replace(",",".")
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
        Player12 = request.form.get("Player12")
        Player13 = request.form.get("Player13")
        Player14 = request.form.get("Player14")
        Player15 = request.form.get("Player15")
        PlayerList = [Player1, Player2, Player3, Player4, Player5, 
                Player6, Player7, Player8, Player9, Player10,
                Player11, Player12, Player13, Player14, Player15]


        if 'Please Select' not in PlayerList:
            Username = session["user"]
            found_user = users11.query.filter_by(username=username).first()

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
            found_user.Player12 = Player12
            found_user.Player13 = Player13
            found_user.Player14 = Player14
            found_user.Player15 = Player15
            db.session.commit()

            form.Budget.data = found_user.Budget
            form.n_tranfers.data = request.form.get("n_tranfers")
            form.Cost1.data = int(fpl_cost[fpl_cost['fpl_name']==Player1]['cost'])/10
            form.Cost2.data = int(fpl_cost[fpl_cost['fpl_name']==Player2]['cost'])/10
            form.Cost3.data = int(fpl_cost[fpl_cost['fpl_name']==Player3]['cost'])/10
            form.Cost4.data = int(fpl_cost[fpl_cost['fpl_name']==Player4]['cost'])/10
            form.Cost5.data = int(fpl_cost[fpl_cost['fpl_name']==Player5]['cost'])/10
            form.Cost6.data = int(fpl_cost[fpl_cost['fpl_name']==Player6]['cost'])/10
            form.Cost7.data = int(fpl_cost[fpl_cost['fpl_name']==Player7]['cost'])/10
            form.Cost8.data = int(fpl_cost[fpl_cost['fpl_name']==Player8]['cost'])/10
            form.Cost9.data = int(fpl_cost[fpl_cost['fpl_name']==Player9]['cost'])/10
            form.Cost10.data = int(fpl_cost[fpl_cost['fpl_name']==Player10]['cost'])/10
            form.Cost11.data = int(fpl_cost[fpl_cost['fpl_name']==Player11]['cost'])/10
            form.Cost12.data = int(fpl_cost[fpl_cost['fpl_name']==Player12]['cost'])/10
            form.Cost13.data = int(fpl_cost[fpl_cost['fpl_name']==Player13]['cost'])/10
            form.Cost14.data = int(fpl_cost[fpl_cost['fpl_name']==Player14]['cost'])/10
            form.Cost15.data = int(fpl_cost[fpl_cost['fpl_name']==Player15]['cost'])/10

            form.n_tranfers.choices = [1,2]
            form.Player1.choices = [(found_user.Player1),"---"]+sorted(fpl_name)
            form.Player2.choices = [(found_user.Player2),"---"]+sorted(fpl_name)
            form.Player3.choices = [(found_user.Player3),"---"]+sorted(fpl_name)
            form.Player4.choices = [(found_user.Player4),"---"]+sorted(fpl_name)
            form.Player5.choices = [(found_user.Player5),"---"]+sorted(fpl_name)
            form.Player6.choices = [(found_user.Player6),"---"]+sorted(fpl_name)
            form.Player7.choices = [(found_user.Player7),"---"]+sorted(fpl_name)
            form.Player8.choices = [(found_user.Player8),"---"]+sorted(fpl_name)
            form.Player9.choices = [(found_user.Player9),"---"]+sorted(fpl_name)
            form.Player10.choices = [(found_user.Player10),"---"]+sorted(fpl_name)
            form.Player11.choices = [(found_user.Player11),"---"]+sorted(fpl_name)
            form.Player12.choices = [(found_user.Player12),"---"]+sorted(fpl_name)
            form.Player13.choices = [(found_user.Player13),"---"]+sorted(fpl_name)
            form.Player14.choices = [(found_user.Player14),"---"]+sorted(fpl_name)
            form.Player15.choices = [(found_user.Player15),"---"]+sorted(fpl_name)        

            return render_template("Viewlist3.html", form=form)  
        else:
    

            form = Form()
            form.n_tranfers.choices = [1,2]
            form.Player1.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player2.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player3.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player4.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player5.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player6.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player7.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player8.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player9.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player10.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player11.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player12.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player13.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player14.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player15.choices = [('Please Select'),"---"]+sorted(fpl_name)
            return render_template("ViewList.html", form=form) 
    else:
        return render_template("ViewList.html", form=form)    
        
@app.route('/Viewlist/',methods=["POST","GET"])
def Viewlist():
    fpl_name = data_final['fpl_name'] 
    username = session["user"]
    found_user = users11.query.filter_by(username=username).first()
    form = Form()
    if request.method == 'GET':  
        if found_user.Player1:
            print("""non empty""")
            print(found_user.Budget)
            form.Budget.data = 0
            form.n_tranfers.choices = [1,2]
            form.Player1.choices = [(found_user.Player1),"---"]+sorted(fpl_name)
            form.Player2.choices = [(found_user.Player2),"---"]+sorted(fpl_name)
            form.Player3.choices = [(found_user.Player3),"---"]+sorted(fpl_name)
            form.Player4.choices = [(found_user.Player4),"---"]+sorted(fpl_name)
            form.Player5.choices = [(found_user.Player5),"---"]+sorted(fpl_name)
            form.Player6.choices = [(found_user.Player6),"---"]+sorted(fpl_name)
            form.Player7.choices = [(found_user.Player7),"---"]+sorted(fpl_name)
            form.Player8.choices = [(found_user.Player8),"---"]+sorted(fpl_name)
            form.Player9.choices = [(found_user.Player9),"---"]+sorted(fpl_name)
            form.Player10.choices = [(found_user.Player10),"---"]+sorted(fpl_name)
            form.Player11.choices = [(found_user.Player11),"---"]+sorted(fpl_name)
            form.Player12.choices = [(found_user.Player12),"---"]+sorted(fpl_name)
            form.Player13.choices = [(found_user.Player13),"---"]+sorted(fpl_name)
            form.Player14.choices = [(found_user.Player14),"---"]+sorted(fpl_name)
            form.Player15.choices = [(found_user.Player15),"---"]+sorted(fpl_name)

        else:
            print("""empty""")
            form = Form()
            form.n_tranfers.choices = [1,2]
            form.Player1.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player2.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player3.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player4.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player5.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player6.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player7.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player8.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player9.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player10.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player11.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player12.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player13.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player14.choices = [('Please Select'),"---"]+sorted(fpl_name)
            form.Player15.choices = [('Please Select'),"---"]+sorted(fpl_name)

    elif request.method == 'POST':
        form.Budget.data = 0
        form.n_tranfers.choices = [1,2]
        form.Player1.choices = [(request.form.get("Player1")),"---"]+sorted(fpl_name)
        form.Player2.choices = [(request.form.get("Player2")),"---"]+sorted(fpl_name)
        form.Player3.choices = [(request.form.get("Player3")),"---"]+sorted(fpl_name)
        form.Player4.choices = [(request.form.get("Player4")),"---"]+sorted(fpl_name)
        form.Player5.choices = [(request.form.get("Player5")),"---"]+sorted(fpl_name)
        form.Player6.choices = [(request.form.get("Player6")),"---"]+sorted(fpl_name)
        form.Player7.choices = [(request.form.get("Player7")),"---"]+sorted(fpl_name)
        form.Player8.choices = [(request.form.get("Player8")),"---"]+sorted(fpl_name)
        form.Player9.choices = [(request.form.get("Player9")),"---"]+sorted(fpl_name)
        form.Player10.choices = [(request.form.get("Player10")),"---"]+sorted(fpl_name)
        form.Player11.choices = [(request.form.get("Player11")),"---"]+sorted(fpl_name)
        form.Player12.choices = [(request.form.get("Player12")),"---"]+sorted(fpl_name)
        form.Player13.choices = [(request.form.get("Player13")),"---"]+sorted(fpl_name)
        form.Player14.choices = [(request.form.get("Player14")),"---"]+sorted(fpl_name)
        form.Player15.choices = [(request.form.get("Player15")),"---"]+sorted(fpl_name)
        print("TES")

        return render_template("ViewList.html", form=form)

    return render_template("ViewList.html", form=form)


@app.route("/login/", methods=["POST","GET"])
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username)
        print(password)
        data_df, bank, rank, transfer = get_current_team(username, password)
        print(data_df)
        if isinstance(data_df, pd.DataFrame):
            print(data_df)
            found_user = users11.query.filter_by(username=form.username.data).first()
            print(found_user)

            if found_user:
                
                print(found_user)
                session.permanent = False
                session["user"] = form.username.data
                session["players"] = data_df.to_json()
                session["bank"] = bank
                session["rank"] = rank
                session["transfer"] = transfer
                print(found_user)
                
                login_user(found_user, remember=form.remember.data)
                print(found_user)

                return redirect(url_for('dashboard'))

            else:
                hashed_password = generate_password_hash(form.password.data, method='sha256')
                new_user = users11(username=form.username.data, email=form.username.data, password=hashed_password,
                    Budget=0, Player1 = '',Player2 = '', Player3 = '', Player4 = '', Player5 = '', Player6 = '',
                    Player7 = '',Player8 = '', Player9 = '', Player10 = '', Player11 = '',Player12 = '',
                    Player13 = '', Player14 = '', Player15 = '')
                db.session.add(new_user)
                db.session.commit()

                session.permanent = True
                session["user"] = form.username.data
                session["players"] = data_df.to_json()
                session["bank"] = bank
                session["rank"] = rank
                session["transfer"] = transfer
                print("hej2")
                login_user(new_user)
                print("dig")
                return redirect(url_for('dashboard'))

        return '<h1>No FPL account</h1>'
        
    print("hej igen")
    return render_template("login.html", form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_user = users11(username=form.username.data, email=form.email.data, password=hashed_password,
                         Budget=0, Player1 = '',Player2 = '', Player3 = '', Player4 = '', Player5 = '', Player6 = '',
                         Player7 = '',Player8 = '', Player9 = '', Player10 = '', Player11 = '',Player12 = '',
                         Player13 = '', Player14 = '', Player15 = '')
        db.session.add(new_user)
        db.session.commit()

        session.permanent = True
        session["user"] = form.username.data
        login_user(new_user)

        return redirect(url_for('dashboard'))
    
    return render_template('signup.html', form=form)

@app.route("/optimization",methods=["POST","GET"])
def optimization():
    
    form = Form()
    data_df = pd.read_json(session["players"])

    Budget_from_players = sum(data_df.selling_price)

    fpl_name = data_final['fpl_name'] 

    PlayerList = list(data_df.player)

    form.Player1IN.choices = [("Please Select"), "---"] + sorted(fpl_name)
    form.Player2IN.choices = [("Please Select"), "---"] + sorted(fpl_name)
    form.Player3IN.choices = [("Please Select"), "---"] + sorted(fpl_name)

    ExcludePlayers = []
    IncludePlayers = []
    ExcludeTeam = []
    IncludePlayers_temp = []
    cash = session["bank"]*10
    n_transfers = session["transfer"] 
    print(Budget_from_players)

    loop_range = 6

    Output_list, TransferCost, nShare, Budget = Pulp_optimization(list(data_final['team']), N, data_final, list(data_final['cost']), list(data_final['cost']), \
                                        list(data_final['Expected_Points_discounted']), list(data_final['position']), ExcludePlayers, IncludePlayers, ExcludeTeam, \
                                        cash, list(data_final['fpl_name']), list(data_final['Expected_Points_round1']), n_transfer, \
                                        PlayerList, sub_1_discount, sub_2_discount,sub_3_discount, sub_gk_discount, Budget_from_players, loop_range)
                                        
    if isinstance(Output_list[0], pd.DataFrame):
        temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[0]['Names'][Output_list[0].player_sub=='player'])]
        temp_0 = Player_stats[Player_stats['fpl_name'].isin(Output_list[0]['Names'][Output_list[0].player_sub=='player'])]

    if isinstance(Output_list[1], pd.DataFrame):
        temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[1]['Names'][Output_list[1].player_sub=='player'])]
        temp_1 = Player_stats[Player_stats['fpl_name'].isin(Output_list[1]['Names'][Output_list[1].player_sub=='player'])]

    if isinstance(Output_list[2], pd.DataFrame):
        temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[2]['Names'][Output_list[2].player_sub=='player'])]
        temp_2 = Player_stats[Player_stats['fpl_name'].isin(Output_list[2]['Names'][Output_list[2].player_sub=='player'])]

    if isinstance(Output_list[3], pd.DataFrame):
        temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[3]['Names'][Output_list[3].player_sub=='player'])]
        temp_3 = Player_stats[Player_stats['fpl_name'].isin(Output_list[3]['Names'][Output_list[3].player_sub=='player'])]

    if isinstance(Output_list[4], pd.DataFrame):
        temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[4]['Names'][Output_list[4].player_sub=='player'])]
        temp_4 = Player_stats[Player_stats['fpl_name'].isin(Output_list[4]['Names'][Output_list[4].player_sub=='player'])]

    if isinstance(Output_list[5], pd.DataFrame):
        temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[5]['Names'][Output_list[5].player_sub=='player'])]
        temp_5 = Player_stats[Player_stats['fpl_name'].isin(Output_list[5]['Names'][Output_list[5].player_sub=='player'])]

    print(Player_stats)
    print(Output_list[0])
    labels = ["Round"+" " + str(current_round),"Round"+" " + str(current_round+1),"Round"+" " + str(current_round+2),"Round"+" " + str(current_round+3),
               "Round"+" " + str(current_round+4),"Round"+" " + str(current_round +5)]
    
    
    values0 = []
    values0_mod = []
    if isinstance(Output_list[0], pd.DataFrame):
        for i in range(6):
            values0.append(round(sum(temp_0.Expected_Points[temp_0['round'] == current_round + i]),1))
            values0_mod.append(round(sum(temp_0.Expected_Points[temp_0['round'] == current_round + i]),1))
            values0_disc = sum(Output_list[0]['xPoints'][Output_list[0].player_sub=='player'])
    else:
        for i in range(6):
            values0.append(0)
            values0_mod.append(0)
            values0_disc = 0

    values1 = []
    values1_mod = []
    if isinstance(Output_list[1], pd.DataFrame):
        for i in range(6):
            values1.append(round(sum(temp_1.Expected_Points[temp_1['round'] == current_round + i]),1))
            values1_mod.append(round(sum(temp_1.Expected_Points[temp_1['round'] == current_round + i]),1))
            values1_disc = sum(Output_list[1]['xPoints'][Output_list[1].player_sub=='player'])
    else:
        for i in range(6):
            values1.append(0)
            values1_mod.append(0)
            values1_disc = 0
        
    values2 = []
    values2_mod = []
    if isinstance(Output_list[2], pd.DataFrame):
        for i in range(6):
            values2.append(round(sum(temp_2.Expected_Points[temp_2['round'] == current_round + i]),1))
            values2_mod.append(round(sum(temp_2.Expected_Points[temp_2['round'] == current_round + i])-(2-n_transfers)*4,1))
            values2_disc = sum(Output_list[2]['xPoints'][Output_list[2].player_sub=='player'])-(2-n_transfers)*4
    else:
        for i in range(6):
            values2.append(0)
            values2_mod.append(0)
            values2_disc = 0

    values3 = []
    values3_mod = []
    if isinstance(Output_list[3], pd.DataFrame):
        for i in range(6):
            values3.append(round(sum(temp_3.Expected_Points[temp_3['round'] == current_round + i]),1))
            values3_mod.append(round(sum(temp_3.Expected_Points[temp_3['round'] == current_round + i])-(3-n_transfers)*4,1))
            values3_disc = sum(Output_list[3]['xPoints'][Output_list[3].player_sub=='player'])-(3-n_transfers)*4
    else:
        for i in range(6):
            values3.append(0)
            values3_mod.append(0)
            values3_disc = 0

    values4 = []
    values4_mod = []
    if isinstance(Output_list[4], pd.DataFrame):
        for i in range(6):
            values4.append(round(sum(temp_4.Expected_Points[temp_4['round'] == current_round + i]),1))
            values4_mod.append(round(sum(temp_4.Expected_Points[temp_4['round'] == current_round + i])-(4-n_transfers)*4,1))
            values4_disc = sum(Output_list[4]['xPoints'][Output_list[4].player_sub=='player'])-(4-n_transfers)*4
    else:
        for i in range(6):
            values4.append(0)
            values4_mod.append(0)
            values4_disc = 0

    values5 = []
    values5_mod = []
    if isinstance(Output_list[5], pd.DataFrame):
        for i in range(6):
            values5.append(round(sum(temp_5.Expected_Points[temp_5['round'] == current_round + i]),1))
            values5_mod.append(round(sum(temp_5.Expected_Points[temp_5['round'] == current_round + i])-(5-n_transfers)*4,1))
            values5_disc = sum(Output_list[5]['xPoints'][Output_list[5].player_sub=='player'])-(5-n_transfers)*4
    else:
        for i in range(6):
            values5.append(0)
            values5_mod.append(0)
            values5_disc = 0

    Name1 = "Expected Points by number of tranfers and rounds (Without tranfer cost)"

    if isinstance(Output_list[1], pd.DataFrame):
        control = [1,2,3,4,5]
    elif isinstance(Output_list[2], pd.DataFrame):
        control = [2,2,3,4,5]
    elif isinstance(Output_list[3], pd.DataFrame):
        control = [3,3,3,4,5]
    elif isinstance(Output_list[4], pd.DataFrame):
        control = [4,4,4,4,5]
    elif isinstance(Output_list[5], pd.DataFrame):
        control = [5,5,5,5,5]

    
    New1, Squad1, Squad_Position1, Squad_Team1, Squad_xPoints1, Squad_Captain1, Expected_points1, buy_list1, \
    buy_list_position1, buy_list_team1, buy_list_xPoints1, buy_list_Cost1,  sell_list1, sell_list_team1, sell_list_position1, sell_list_xPoints1, sell_list_Cost1 = get_optim_results(Output_list[control[0]], PlayerList, data_final)

    New2, Squad2, Squad_Position2, Squad_Team2, Squad_xPoints2, Squad_Captain2, Expected_points2, buy_list2, \
    buy_list_position2, buy_list_team2, buy_list_xPoints2, buy_list_Cost2,  sell_list2, sell_list_team2, sell_list_position2, sell_list_xPoints2, sell_list_Cost2 = get_optim_results(Output_list[control[1]], PlayerList, data_final)

    New3, Squad3, Squad_Position3, Squad_Team3, Squad_xPoints3, Squad_Captain3, Expected_points3, buy_list3, \
    buy_list_position3, buy_list_team3, buy_list_xPoints3, buy_list_Cost3,  sell_list3, sell_list_team3, sell_list_position3, sell_list_xPoints3, sell_list_Cost3 = get_optim_results(Output_list[control[2]], PlayerList, data_final)

    New4, Squad4, Squad_Position4, Squad_Team4, Squad_xPoints4, Squad_Captain4, Expected_points4, buy_list4, \
    buy_list_position4, buy_list_team4, buy_list_xPoints4, buy_list_Cost4,  sell_list4, sell_list_team4, sell_list_position4, sell_list_xPoints4, sell_list_Cost4 = get_optim_results(Output_list[control[3]], PlayerList, data_final)

    New5, Squad5, Squad_Position5, Squad_Team5, Squad_xPoints5, Squad_Captain5, Expected_points5, buy_list5, \
    buy_list_position5, buy_list_team5, buy_list_xPoints5, buy_list_Cost5,  sell_list5, sell_list_team5, sell_list_position5, sell_list_xPoints5, sell_list_Cost5 = get_optim_results(Output_list[control[4]], PlayerList, data_final)

    Output = Output_list[5]

    TransferCost = TransferCost[1]
    max_val = max([values0_disc,values1_disc,values2_disc,values3_disc,values4_disc,values5_disc])
    if values0_disc==max_val:
        substitues = 0
        buy_str = 'None'
        sell_str = 'None'
        captain = 'None'
        vice_captain = 'None'
    elif values1_disc==max_val:
        substitues = 1
        buy_str = ' '.join([str(item) for item in buy_list1])
        sell_str = ' '.join([str(item) for item in sell_list1])
        captain =  pd.DataFrame(Squad1)[pd.DataFrame(Squad_Captain1) == 'Captain'].dropna()[0].iloc[0]
        temp = pd.DataFrame(Squad_xPoints1).sort_values(by=0)
        length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
        vice_captain =  pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0].iloc[length]
    elif values2_disc==max_val:
        substitues = 2
        buy_str = ' '.join([str(item) for item in buy_list2])
        sell_str = ' '.join([str(item) for item in sell_list2])
        captain =  pd.DataFrame(Squad2)[pd.DataFrame(Squad_Captain2) == 'Captain'].dropna()[0].iloc[0]
        temp = pd.DataFrame(Squad_xPoints2).sort_values(by=0)
        length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
        vice_captain = pd.DataFrame(Squad2)[pd.DataFrame(Squad_xPoints2) == float(temp.iloc[-2])].dropna()[0].iloc[length]
        print(pd.DataFrame(Squad2)[pd.DataFrame(Squad_xPoints2) == float(temp.iloc[-2])].dropna()[0])
    elif values3_disc==max_val:
        substitues = 3
        buy_str = ' '.join([str(item) for item in buy_list3])
        sell_str = ' '.join([str(item) for item in sell_list3])
        captain =  pd.DataFrame(Squad3)[pd.DataFrame(Squad_Captain3) == 'Captain'].dropna()[0].iloc[0]
        temp = pd.DataFrame(Squad_xPoints3).sort_values(by=0)
        print(pd.DataFrame(Squad3)[pd.DataFrame(Squad_xPoints3) == float(temp.iloc[-2])].dropna()[0])
        length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
        vice_captain =  pd.DataFrame(Squad3)[pd.DataFrame(Squad_xPoints3) == float(temp.iloc[-2])].dropna()[0].iloc[length]
    elif values4_disc==max_val:
        substitues = 4
        buy_str = ' '.join([str(item) for item in buy_list4])
        sell_str = ' '.join([str(item) for item in sell_list4])
        captain = pd.DataFrame(Squad4)[pd.DataFrame(Squad_Captain4) == 'Captain'].dropna()[0].iloc[0]
        temp = pd.DataFrame(Squad_xPoints4).sort_values(by=0)
        length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
        vice_captain =  pd.DataFrame(Squad4)[pd.DataFrame(Squad_xPoints4) == float(temp.iloc[-2])].dropna()[0].iloc[length]
    else:
        substitues = 5
        buy_str = ' '.join([str(item) for item in buy_list5])
        sell_str = ' '.join([str(item) for item in sell_list5])
        captain =  pd.DataFrame(Squad5)[pd.DataFrame(Squad_Captain5) == 'Captain'].dropna()[0].iloc[0]
        temp = pd.DataFrame(Squad_xPoints5).sort_values(by=0)
        length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
        vice_captain =  pd.DataFrame(Squad5)[pd.DataFrame(Squad_xPoints5) == float(temp.iloc[-2])].dropna()[0].iloc[length]

    if isinstance(Output, pd.DataFrame):

        if 'Please Select' in ExcludePlayers:
            ExcludePlayers = (value for value in ExcludePlayers if value != 'Please Select')
        if 'Please Select' in ExcludeTeam:
            ExcludeTeam = (value for value in ExcludeTeam if value != 'Please Select')   
        print(values0)

        return render_template("Dashboard2.html", 
                                ExcludePlayers  = ExcludePlayers, ExcludeTeam = ExcludeTeam, Expected_points = Expected_points1, 
                                Squad1 = Squad1, Squad_Position1 = Squad_Position1 ,Squad_Team1 = Squad_Team1, Squad_xPoints1 = Squad_xPoints1, Squad_Captain1 = Squad_Captain1, 
                                buy_list1=buy_list1, sell_list1=sell_list1, buy_list_position1=buy_list_position1, buy_list_team1=buy_list_team1, buy_list_xPoints1=buy_list_xPoints1,
                                sell_list_team1=sell_list_team1, sell_list_position1=sell_list_position1, sell_list_xPoints1=sell_list_xPoints1,New1 = New1, buy_list_Cost1 = buy_list_Cost1, sell_list_Cost1 = sell_list_Cost1, 
                                Squad2 = Squad2, Squad_Position2 = Squad_Position2 ,Squad_Team2 = Squad_Team2, Squad_xPoints2 = Squad_xPoints2, Squad_Captain2 = Squad_Captain2, 
                                buy_list2=buy_list2, sell_list2=sell_list2, buy_list_position2=buy_list_position2, buy_list_team2=buy_list_team2, buy_list_xPoints2=buy_list_xPoints2,
                                sell_list_team2=sell_list_team2, sell_list_position2=sell_list_position2, sell_list_xPoints2=sell_list_xPoints2,New2 = New2, buy_list_Cost2 = buy_list_Cost2, sell_list_Cost2 = sell_list_Cost2,
                                Squad3 = Squad3, Squad_Position3 = Squad_Position3 ,Squad_Team3 = Squad_Team3, Squad_xPoints3 = Squad_xPoints3, Squad_Captain3 = Squad_Captain3, 
                                buy_list3=buy_list3, sell_list3=sell_list3, buy_list_position3=buy_list_position3, buy_list_team3=buy_list_team3, buy_list_xPoints3=buy_list_xPoints3,
                                sell_list_team3=sell_list_team3, sell_list_position3=sell_list_position3, sell_list_xPoints3=sell_list_xPoints3,New3 = New3, buy_list_Cost3 = buy_list_Cost3, sell_list_Cost3 = sell_list_Cost3,
                                Squad4 = Squad4, Squad_Position4 = Squad_Position4 ,Squad_Team4 = Squad_Team4, Squad_xPoints4 = Squad_xPoints4, Squad_Captain4 = Squad_Captain4, 
                                buy_list4=buy_list4, sell_list4=sell_list4, buy_list_position4=buy_list_position4, buy_list_team4=buy_list_team4, buy_list_xPoints4=buy_list_xPoints4,
                                sell_list_team4=sell_list_team4, sell_list_position4=sell_list_position4, sell_list_xPoints4=sell_list_xPoints4,New4 = New4, buy_list_Cost4 = buy_list_Cost4, sell_list_Cost4 = sell_list_Cost4,
                                Squad5 = Squad5, Squad_Position5 = Squad_Position5 ,Squad_Team5 = Squad_Team5, Squad_xPoints5 = Squad_xPoints5, Squad_Captain5 = Squad_Captain5, 
                                buy_list5=buy_list5, sell_list5=sell_list5, buy_list_position5=buy_list_position5, buy_list_team5=buy_list_team5, buy_list_xPoints5=buy_list_xPoints5,
                                sell_list_team5=sell_list_team5, sell_list_position5=sell_list_position5, sell_list_xPoints5=sell_list_xPoints5,New5 = New5, buy_list_Cost5 = buy_list_Cost5, sell_list_Cost5 = sell_list_Cost5,
                                form = form, labels=labels, values0=values0, values1=values1, values2=values2, values3=values3, values4=values4, values5=values5,
                                values0_mod=values0_mod, values1_mod=values1_mod, values2_mod=values2_mod, values3_mod=values3_mod, values4_mod=values4_mod, values5_mod=values5_mod,
                                Name1=Name1, n_transfers = n_transfers, substitues = substitues, buy_str = buy_str, sell_str = sell_str, captain = captain, vice_captain = vice_captain, IncludePlayers_temp = IncludePlayers_temp)   

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
        return render_template('fail.html', name=current_user.username, Squad = Squad, Squad_Position = Squad_Position ,Squad_Team = Squad_Team, 
                                        Squad_xPoints = Squad_xPoints, Squad_Captain = Squad_Captain, labels=labels, values=values,
                                        nShare = nShare, Budget = Budget,error_statement=error_statement)
    
    
@app.route("/teamupdated", methods=["POST"])
def teamupdated():
    
    Squad = request.form.getlist("Name")
    Budget = request.form.getlist("Budget")
    username = session["user"]
    found_user = users11.query.filter_by(username=username).first()

    found_user.Player1 = Squad[0]
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
    found_user.Player12 = Squad[11]
    found_user.Player13 = Squad[12]
    found_user.Player14 = Squad[13]
    found_user.Player15 = Squad[14]

    db.session.commit()    
    
    return redirect(url_for('dashboard'))

@app.route("/Adjustoptimization", methods=["POST"])
def sure():
    if request.method == 'POST':    
      

        sell1 = request.form.getlist("sell1")
        sell2 = request.form.getlist("sell2")
        sell3 = request.form.getlist("sell3")
        sell4 = request.form.getlist("sell4")
        sell5 = request.form.getlist("sell5")
        mycheckboxsell1 = request.form.getlist("mycheckboxsell1")
        mycheckboxsell2 = request.form.getlist("mycheckboxsell2")
        mycheckboxsell3 = request.form.getlist("mycheckboxsell3")
        mycheckboxsell4 = request.form.getlist("mycheckboxsell4")
        mycheckboxsell5 = request.form.getlist("mycheckboxsell5")

        buy1 = request.form.getlist("buy1")
        buy2 = request.form.getlist("buy2")
        buy3 = request.form.getlist("buy2")
        buy4 = request.form.getlist("buy4")
        buy5 = request.form.getlist("buy5")
        mycheckboxbuy1 = request.form.getlist("mycheckboxbuy1")
        mycheckboxbuy2 = request.form.getlist("mycheckboxbuy2")
        mycheckboxbuy3 = request.form.getlist("mycheckboxbuy3")
        mycheckboxbuy4 = request.form.getlist("mycheckboxbuy4")
        mycheckboxbuy5 = request.form.getlist("mycheckboxbuy5")

        included1 = request.form.getlist("mycheckbox1")
        includedTeams1 = request.form.getlist("mycheckboxteam1")
        included2 = request.form.getlist("mycheckbox2")
        includedTeams2 = request.form.getlist("mycheckboxteam2")
        included3 = request.form.getlist("mycheckbox3")
        includedTeams3 = request.form.getlist("mycheckboxteam3")
        included4 = request.form.getlist("mycheckbox4")
        includedTeams4 = request.form.getlist("mycheckboxteam4")
        included5 = request.form.getlist("mycheckbox5")
        includedTeams5 = request.form.getlist("mycheckboxteam5")
        suggested_players1 = request.form.getlist("Names1")
        suggested_teams1 = request.form.getlist("Teams1")
        suggested_players2 = request.form.getlist("Names2")
        suggested_teams2 = request.form.getlist("Teams2")
        suggested_players3 = request.form.getlist("Names3")
        suggested_teams3 = request.form.getlist("Teams3")
        suggested_players4 = request.form.getlist("Names4")
        suggested_teams4 = request.form.getlist("Teams4")
        suggested_players5 = request.form.getlist("Names5")
        suggested_teams5 = request.form.getlist("Teams5")
        excludedP = request.form.getlist("mycheckboxExcludePLayer")
        excludedPlayers = request.form.getlist("ExcludedPlayers")
        excludedT = request.form.getlist("mycheckboxExcludedTeams")
        excludedTeams = request.form.getlist("ExcludedTeams")
        n_transfers = request.form.getlist("n_transfers")
        IncludePlayers_temp_checkbox = request.form.getlist("IncludePlayers_temp_checkbox")
        IncludePlayers_temp_val = request.form.getlist("IncludePlayers_temp_val")



        ExcludePlayers = []
        IncludePlayers_temp = []
        IncludePlayers = []
        ExcludeTeam = []

## from input output table 
        for i in range(len(sell1)):
            if str(i+1) in mycheckboxsell1:
                IncludePlayers_temp.append(sell1[i]) 

        for i in range(len(sell2)):
            if str(i+1) in mycheckboxsell2:
                IncludePlayers_temp.append(sell2[i]) 

        for i in range(len(sell3)):
            if str(i+1) in mycheckboxsell3:
                IncludePlayers_temp.append(sell3[i]) 

        for i in range(len(sell4)):
            if str(i+1) in mycheckboxsell4:
                IncludePlayers_temp.append(sell4[i]) 

        for i in range(len(sell5)):
            if str(i+1) in mycheckboxsell5:
                IncludePlayers_temp.append(sell5[i]) 

        for i in range(len(buy1)):
            if str(i+1) in mycheckboxbuy1:
                ExcludePlayers.append(buy1[i]) 

        for i in range(len(buy2)):
            if str(i+1) in mycheckboxbuy2:
                ExcludePlayers.append(buy2[i]) 

        for i in range(len(buy3)):
            if str(i+1) in mycheckboxbuy3:
                ExcludePlayers.append(buy3[i]) 

        for i in range(len(buy4)):
            if str(i+1) in mycheckboxbuy4:
                ExcludePlayers.append(buy4[i]) 

        for i in range(len(buy5)):
            if str(i+1) in mycheckboxbuy5:
                ExcludePlayers.append(buy5[i]) 
## From team overview

        for i in range(len(suggested_players1)):
            if str(i+1) in included1:
                ExcludePlayers.append(suggested_players1[i]) 

        for i in range(len(suggested_players2)):
            if str(i+1) in included2:
                ExcludePlayers.append(suggested_players2[i]) 

        for i in range(len(suggested_players3)):
            if str(i+1) in included3:
                ExcludePlayers.append(suggested_players3[i]) 

        for i in range(len(suggested_players4)):
            if str(i+1) in included4:
                ExcludePlayers.append(suggested_players4[i]) 

        for i in range(len(suggested_players5)):
            if str(i+1) in included5:
                ExcludePlayers.append(suggested_players5[i]) 

        for i in range(len(suggested_teams1)):
            if str(i+1) in includedTeams1:
                ExcludeTeam.append(suggested_teams1[i]) 

        for i in range(len(suggested_teams2)):
            if str(i+1) in includedTeams2:
                ExcludeTeam.append(suggested_teams2[i]) 

        for i in range(len(suggested_teams3)):
            if str(i+1) in includedTeams3:
                ExcludeTeam.append(suggested_teams3[i]) 

        for i in range(len(suggested_teams4)):
            if str(i+1) in includedTeams4:
                ExcludeTeam.append(suggested_teams4[i]) 

        for i in range(len(suggested_teams5)):
            if str(i+1) in includedTeams5:
                ExcludeTeam.append(suggested_teams5[i]) 

        print(range(len(excludedPlayers)))    
        for i in range(len(excludedPlayers)):
            if str(i+1) in excludedP:
                ExcludePlayers.append(excludedPlayers[i]) 

        for i in range(len(excludedTeams)):
            if str(i+1) in excludedT:
                ExcludeTeam.append(excludedTeams[i]) 

        for i in range(len(IncludePlayers_temp_val)):
            if str(i+1) in IncludePlayers_temp_checkbox:
                IncludePlayers_temp.append(IncludePlayers_temp_val[i]) 
        
        
        Player1_IN = request.form.get("Player1IN")
        Player2_IN = request.form.get("Player2IN")
        Player3_IN = request.form.get("Player3IN")

        form = Form()
        
        fpl_name = data_final['fpl_name'] 

        if Player1_IN != "Please Select":
            IncludePlayers.append(Player1_IN)
            form.Player1IN.choices = [(Player1_IN),"None"]+sorted(fpl_name)
        else:
            form.Player1IN.choices = [("Please Select"),"None"]+sorted(fpl_name)

        if Player2_IN != "Please Select":
            IncludePlayers.append(Player2_IN)
            form.Player2IN.choices = [(Player2_IN),"None"]+sorted(fpl_name)
        else:
            form.Player2IN.choices = [("Please Select"),"None"]+sorted(fpl_name)

        if Player3_IN != "Please Select":
            IncludePlayers.append(Player3_IN)
            form.Player3IN.choices = [(Player3_IN),"None"]+sorted(fpl_name)
        else:
            form.Player3IN.choices = [("Please Select"),"None"]+sorted(fpl_name)

        for i in IncludePlayers_temp:
            IncludePlayers.append(i)

        print(ExcludePlayers)
        print(IncludePlayers)
        print(ExcludeTeam)

        data_df = pd.read_json(session["players"])
        Budget_from_players = sum(data_df.selling_price)
        PlayerList = list(data_df.player)
        cash = session["bank"]*10
        n_transfers = session["transfer"] 
        print(Budget_from_players)
        print(Budget_from_players)
        loop_range = 6

        Output_list, TransferCost, nShare, Budget = Pulp_optimization(list(data_final['team']), N, data_final, list(data_final['cost']), list(data_final['cost']), \
                                            list(data_final['Expected_Points_discounted']), list(data_final['position']), ExcludePlayers, IncludePlayers, ExcludeTeam, \
                                            cash, list(data_final['fpl_name']), list(data_final['Expected_Points_round1']), n_transfer, \
                                            PlayerList, sub_1_discount, sub_2_discount,sub_3_discount, sub_gk_discount, Budget_from_players, loop_range)
                                            
        print(Output_list)
        if isinstance(Output_list[0], pd.DataFrame):
            temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[0]['Names'][Output_list[0].player_sub=='player'])]
            temp_0 = Player_stats[Player_stats['fpl_name'].isin(Output_list[0]['Names'][Output_list[0].player_sub=='player'])]

        if isinstance(Output_list[1], pd.DataFrame):
            temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[1]['Names'][Output_list[1].player_sub=='player'])]
            temp_1 = Player_stats[Player_stats['fpl_name'].isin(Output_list[1]['Names'][Output_list[1].player_sub=='player'])]

        if isinstance(Output_list[2], pd.DataFrame):
            temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[2]['Names'][Output_list[2].player_sub=='player'])]
            temp_2 = Player_stats[Player_stats['fpl_name'].isin(Output_list[2]['Names'][Output_list[2].player_sub=='player'])]

        if isinstance(Output_list[3], pd.DataFrame):
            temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[3]['Names'][Output_list[3].player_sub=='player'])]
            temp_3 = Player_stats[Player_stats['fpl_name'].isin(Output_list[3]['Names'][Output_list[3].player_sub=='player'])]

        if isinstance(Output_list[4], pd.DataFrame):
            temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[4]['Names'][Output_list[4].player_sub=='player'])]
            temp_4 = Player_stats[Player_stats['fpl_name'].isin(Output_list[4]['Names'][Output_list[4].player_sub=='player'])]

        if isinstance(Output_list[5], pd.DataFrame):
            temp = Player_stats[Player_stats['fpl_name'].isin(Output_list[5]['Names'][Output_list[5].player_sub=='player'])]
            temp_5 = Player_stats[Player_stats['fpl_name'].isin(Output_list[5]['Names'][Output_list[5].player_sub=='player'])]

        print(Player_stats)
        print(Output_list[0])
        labels = ["Round"+" " + str(current_round),"Round"+" " + str(current_round+1),"Round"+" " + str(current_round+2),"Round"+" " + str(current_round+3),
                "Round"+" " + str(current_round+4),"Round"+" " + str(current_round +5)]
        
        
        values0 = []
        values0_mod = []
        if isinstance(Output_list[0], pd.DataFrame):
            for i in range(6):
                values0.append(round(sum(temp_0.Expected_Points[temp_0['round'] == current_round + i]),1))
                values0_mod.append(round(sum(temp_0.Expected_Points[temp_0['round'] == current_round + i]),1))
                values0_disc = sum(Output_list[0]['xPoints'][Output_list[0].player_sub=='player'])
        else:
            for i in range(6):
                values0.append(0)
                values0_mod.append(0)
                values0_disc = 0

        values1 = []
        values1_mod = []
        if isinstance(Output_list[1], pd.DataFrame):
            for i in range(6):
                values1.append(round(sum(temp_1.Expected_Points[temp_1['round'] == current_round + i]),1))
                values1_mod.append(round(sum(temp_1.Expected_Points[temp_1['round'] == current_round + i]),1))
                values1_disc = sum(Output_list[1]['xPoints'][Output_list[1].player_sub=='player'])
        else:
            for i in range(6):
                values1.append(0)
                values1_mod.append(0)
                values1_disc = 0
            
        values2 = []
        values2_mod = []
        if isinstance(Output_list[2], pd.DataFrame):
            for i in range(6):
                values2.append(round(sum(temp_2.Expected_Points[temp_2['round'] == current_round + i]),1))
                values2_mod.append(round(sum(temp_2.Expected_Points[temp_2['round'] == current_round + i])-(2-n_transfers)*4,1))
                values2_disc = sum(Output_list[2]['xPoints'][Output_list[2].player_sub=='player'])-(2-n_transfers)*4
        else:
            for i in range(6):
                values2.append(0)
                values2_mod.append(0)
                values2_disc = 0

        values3 = []
        values3_mod = []
        if isinstance(Output_list[3], pd.DataFrame):
            for i in range(6):
                values3.append(round(sum(temp_3.Expected_Points[temp_3['round'] == current_round + i]),1))
                values3_mod.append(round(sum(temp_3.Expected_Points[temp_3['round'] == current_round + i])-(3-n_transfers)*4,1))
                values3_disc = sum(Output_list[3]['xPoints'][Output_list[3].player_sub=='player'])-(3-n_transfers)*4
        else:
            for i in range(6):
                values3.append(0)
                values3_mod.append(0)
                values3_disc = 0

        values4 = []
        values4_mod = []
        if isinstance(Output_list[4], pd.DataFrame):
            for i in range(6):
                values4.append(round(sum(temp_4.Expected_Points[temp_4['round'] == current_round + i]),1))
                values4_mod.append(round(sum(temp_4.Expected_Points[temp_4['round'] == current_round + i])-(4-n_transfers)*4,1))
                values4_disc = sum(Output_list[4]['xPoints'][Output_list[4].player_sub=='player'])-(4-n_transfers)*4
        else:
            for i in range(6):
                values4.append(0)
                values4_mod.append(0)
                values4_disc = 0

        values5 = []
        values5_mod = []
        if isinstance(Output_list[5], pd.DataFrame):
            for i in range(6):
                values5.append(round(sum(temp_5.Expected_Points[temp_5['round'] == current_round + i]),1))
                values5_mod.append(round(sum(temp_5.Expected_Points[temp_5['round'] == current_round + i])-(5-n_transfers)*4,1))
                values5_disc = sum(Output_list[5]['xPoints'][Output_list[5].player_sub=='player'])-(5-n_transfers)*4
        else:
            for i in range(6):
                values5.append(0)
                values5_mod.append(0)
                values5_disc = 0


        Name1 = "Expected Points by number of tranfers and rounds (Without tranfer cost)"
        
        if isinstance(Output_list[1], pd.DataFrame):
            control = [1,2,3,4,5]
        elif isinstance(Output_list[2], pd.DataFrame):
            control = [2,2,3,4,5]
        elif isinstance(Output_list[3], pd.DataFrame):
            control = [3,3,3,4,5]
        elif isinstance(Output_list[4], pd.DataFrame):
            control = [4,4,4,4,5]
        elif isinstance(Output_list[5], pd.DataFrame):
            control = [5,5,5,5,5]

        New1, Squad1, Squad_Position1, Squad_Team1, Squad_xPoints1, Squad_Captain1, Expected_points1, buy_list1, \
        buy_list_position1, buy_list_team1, buy_list_xPoints1, buy_list_Cost1,  sell_list1, sell_list_team1, sell_list_position1, sell_list_xPoints1, sell_list_Cost1 = get_optim_results(Output_list[control[0]], PlayerList, data_final)

        New2, Squad2, Squad_Position2, Squad_Team2, Squad_xPoints2, Squad_Captain2, Expected_points2, buy_list2, \
        buy_list_position2, buy_list_team2, buy_list_xPoints2, buy_list_Cost2,  sell_list2, sell_list_team2, sell_list_position2, sell_list_xPoints2, sell_list_Cost2 = get_optim_results(Output_list[control[1]], PlayerList, data_final)

        New3, Squad3, Squad_Position3, Squad_Team3, Squad_xPoints3, Squad_Captain3, Expected_points3, buy_list3, \
        buy_list_position3, buy_list_team3, buy_list_xPoints3, buy_list_Cost3,  sell_list3, sell_list_team3, sell_list_position3, sell_list_xPoints3, sell_list_Cost3 = get_optim_results(Output_list[control[2]], PlayerList, data_final)

        New4, Squad4, Squad_Position4, Squad_Team4, Squad_xPoints4, Squad_Captain4, Expected_points4, buy_list4, \
        buy_list_position4, buy_list_team4, buy_list_xPoints4, buy_list_Cost4,  sell_list4, sell_list_team4, sell_list_position4, sell_list_xPoints4, sell_list_Cost4 = get_optim_results(Output_list[control[3]], PlayerList, data_final)

        New5, Squad5, Squad_Position5, Squad_Team5, Squad_xPoints5, Squad_Captain5, Expected_points5, buy_list5, \
        buy_list_position5, buy_list_team5, buy_list_xPoints5, buy_list_Cost5,  sell_list5, sell_list_team5, sell_list_position5, sell_list_xPoints5, sell_list_Cost5 = get_optim_results(Output_list[control[4]], PlayerList, data_final)

        Output = Output_list[3]

        TransferCost = TransferCost[1]

        max_val = max([values0_disc,values1_disc,values2_disc,values3_disc,values4_disc,values5_disc])
        if values0_disc==max_val:
            substitues = 0
            buy_str = 'None'
            sell_str = 'None'
            captain = 'None'
            vice_captain = 'None'
        elif values1_disc==max_val:
            substitues = 1
            buy_str = ' '.join([str(item) for item in buy_list1])
            sell_str = ' '.join([str(item) for item in sell_list1])
            captain =  pd.DataFrame(Squad1)[pd.DataFrame(Squad_Captain1) == 'Captain'].dropna()[0].iloc[0]
            temp = pd.DataFrame(Squad_xPoints1).sort_values(by=0)
            length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
            vice_captain =  pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0].iloc[length]
        elif values2_disc==max_val:
            substitues = 2
            buy_str = ' '.join([str(item) for item in buy_list2])
            sell_str = ' '.join([str(item) for item in sell_list2])
            captain =  pd.DataFrame(Squad2)[pd.DataFrame(Squad_Captain2) == 'Captain'].dropna()[0].iloc[0]
            temp = pd.DataFrame(Squad_xPoints2).sort_values(by=0)
            length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
            vice_captain = pd.DataFrame(Squad2)[pd.DataFrame(Squad_xPoints2) == float(temp.iloc[-2])].dropna()[0].iloc[length]
            print(pd.DataFrame(Squad2)[pd.DataFrame(Squad_xPoints2) == float(temp.iloc[-2])].dropna()[0])
        elif values3_disc==max_val:
            substitues = 3
            buy_str = ' '.join([str(item) for item in buy_list3])
            sell_str = ' '.join([str(item) for item in sell_list3])
            captain =  pd.DataFrame(Squad3)[pd.DataFrame(Squad_Captain3) == 'Captain'].dropna()[0].iloc[0]
            temp = pd.DataFrame(Squad_xPoints3).sort_values(by=0)
            print(pd.DataFrame(Squad3)[pd.DataFrame(Squad_xPoints3) == float(temp.iloc[-2])].dropna()[0])
            length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
            vice_captain =  pd.DataFrame(Squad3)[pd.DataFrame(Squad_xPoints3) == float(temp.iloc[-2])].dropna()[0].iloc[length]
        elif values4_disc==max_val:
            substitues = 4
            buy_str = ' '.join([str(item) for item in buy_list4])
            sell_str = ' '.join([str(item) for item in sell_list4])
            captain = pd.DataFrame(Squad4)[pd.DataFrame(Squad_Captain4) == 'Captain'].dropna()[0].iloc[0]
            temp = pd.DataFrame(Squad_xPoints4).sort_values(by=0)
            length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
            vice_captain =  pd.DataFrame(Squad4)[pd.DataFrame(Squad_xPoints4) == float(temp.iloc[-2])].dropna()[0].iloc[length]
        else:
            substitues = 5
            buy_str = ' '.join([str(item) for item in buy_list5])
            sell_str = ' '.join([str(item) for item in sell_list5])
            captain =  pd.DataFrame(Squad5)[pd.DataFrame(Squad_Captain5) == 'Captain'].dropna()[0].iloc[0]
            temp = pd.DataFrame(Squad_xPoints5).sort_values(by=0)
            length = len(pd.DataFrame(Squad1)[pd.DataFrame(Squad_xPoints1) == float(temp.iloc[-2])].dropna()[0])-1
            vice_captain =  pd.DataFrame(Squad5)[pd.DataFrame(Squad_xPoints5) == float(temp.iloc[-2])].dropna()[0].iloc[length]

        return render_template("Dashboard2.html", 
                                        ExcludePlayers  = ExcludePlayers, ExcludeTeam = ExcludeTeam, Expected_points = Expected_points1, 
                                        Squad1 = Squad1, Squad_Position1 = Squad_Position1 ,Squad_Team1 = Squad_Team1, Squad_xPoints1 = Squad_xPoints1, Squad_Captain1 = Squad_Captain1, 
                                        buy_list1=buy_list1, sell_list1=sell_list1, buy_list_position1=buy_list_position1, buy_list_team1=buy_list_team1, buy_list_xPoints1=buy_list_xPoints1,
                                        sell_list_team1=sell_list_team1, sell_list_position1=sell_list_position1, sell_list_xPoints1=sell_list_xPoints1,New1 = New1, buy_list_Cost1 = buy_list_Cost1, sell_list_Cost1 = sell_list_Cost1, 
                                        Squad2 = Squad2, Squad_Position2 = Squad_Position2 ,Squad_Team2 = Squad_Team2, Squad_xPoints2 = Squad_xPoints2, Squad_Captain2 = Squad_Captain2, 
                                        buy_list2=buy_list2, sell_list2=sell_list2, buy_list_position2=buy_list_position2, buy_list_team2=buy_list_team2, buy_list_xPoints2=buy_list_xPoints2,
                                        sell_list_team2=sell_list_team2, sell_list_position2=sell_list_position2, sell_list_xPoints2=sell_list_xPoints2,New2 = New2, buy_list_Cost2 = buy_list_Cost2, sell_list_Cost2 = sell_list_Cost2,
                                        Squad3 = Squad3, Squad_Position3 = Squad_Position3 ,Squad_Team3 = Squad_Team3, Squad_xPoints3 = Squad_xPoints3, Squad_Captain3 = Squad_Captain3, 
                                        buy_list3=buy_list3, sell_list3=sell_list3, buy_list_position3=buy_list_position3, buy_list_team3=buy_list_team3, buy_list_xPoints3=buy_list_xPoints3,
                                        sell_list_team3=sell_list_team3, sell_list_position3=sell_list_position3, sell_list_xPoints3=sell_list_xPoints3,New3 = New3, buy_list_Cost3 = buy_list_Cost3, sell_list_Cost3 = sell_list_Cost3,
                                        Squad4 = Squad4, Squad_Position4 = Squad_Position4 ,Squad_Team4 = Squad_Team4, Squad_xPoints4 = Squad_xPoints4, Squad_Captain4 = Squad_Captain4, 
                                        buy_list4=buy_list4, sell_list4=sell_list4, buy_list_position4=buy_list_position4, buy_list_team4=buy_list_team4, buy_list_xPoints4=buy_list_xPoints4,
                                        sell_list_team4=sell_list_team4, sell_list_position4=sell_list_position4, sell_list_xPoints4=sell_list_xPoints4,New4 = New4, buy_list_Cost4 = buy_list_Cost4, sell_list_Cost4 = sell_list_Cost4,
                                        Squad5 = Squad5, Squad_Position5 = Squad_Position5 ,Squad_Team5 = Squad_Team5, Squad_xPoints5 = Squad_xPoints5, Squad_Captain5 = Squad_Captain5, 
                                        buy_list5=buy_list5, sell_list5=sell_list5, buy_list_position5=buy_list_position5, buy_list_team5=buy_list_team5, buy_list_xPoints5=buy_list_xPoints5,
                                        sell_list_team5=sell_list_team5, sell_list_position5=sell_list_position5, sell_list_xPoints5=sell_list_xPoints5,New5 = New5, buy_list_Cost5 = buy_list_Cost5, sell_list_Cost5 = sell_list_Cost5,
                                        form = form, labels=labels, values0=values0, values1=values1, values2=values2, values3=values3, values4=values4, values5=values5,
                                        values0_mod=values0_mod, values1_mod=values1_mod, values2_mod=values2_mod, values3_mod=values3_mod, values4_mod=values4_mod, values5_mod=values5_mod,
                                        Name1=Name1, n_transfers = n_transfers, substitues = substitues, buy_str = buy_str, sell_str = sell_str, captain = captain, vice_captain = vice_captain, IncludePlayers_temp = IncludePlayers_temp)   
                                                            
@app.route('/dashboard2')
def dashboard2():
    return render_template('dashboard2.html')
    
@app.route('/dashboard')
@login_required
def dashboard():

    username = session["user"]
    data_df = pd.read_json(session["players"])
    
    Squad = list(data_df['player'])
    Squad_Position = list(data_df['position'])
    Squad_Team = list(data_df['team'])
    Squad_xPoints = list(data_df['Expected_Points_round1'])
    
    Squad_Captain = list(data_df['Captain'])
    
    squad_points = round(sum(data_df['Expected_Points_round1']),1)
    data_df = pd.read_json(session["players"])
    Budget_from_players = sum(data_df.selling_price)
    PlayerList = list(data_df.player)
    cash = session["bank"]*10
    
    Output_list, TransferCost, nShare, Budget = Pulp_optimization(list(data_final['team']), N, data_final, list(data_final['cost']), list(data_final['cost']), \
                                                                    list(data_final['Expected_Points_discounted']), list(data_final['position']), [], [], [], \
                                                                    cash, list(data_final['fpl_name']), list(data_final['Expected_Points_round1']), n_transfer, \
                                                                    PlayerList, sub_1_discount, sub_2_discount,sub_3_discount, sub_gk_discount, Budget_from_players, 1)

    New1, Squad1, Squad_Position1, Squad_Team1, Squad_xPoints1, Squad_Captain1, Expected_points1, buy_list1, \
        buy_list_position1, buy_list_team1, buy_list_xPoints1, buy_list_cost1, sell_list1, sell_list_team1, sell_list_position1, sell_list_xPoints1, sell_list_cost1,= get_optim_results(Output_list[0], PlayerList, data_final)
    
    buy_list1 =  buy_list1[0]
    sell_list1 =  sell_list1[0]
    point_increase = round(sum(buy_list_xPoints1) - sum(sell_list_xPoints1),2)
    print(sell_list1)
    zero_players = sum(data_df['Expected_Points_round1'] == 0)
    zero_players_bench = sum(((data_df['Expected_Points_round1'] == 0) & (data_df['multiplier'] == 1)))
    rank = session["rank"]
    n_transfers = session["transfer"]

    xPoints = list(round(data_final['Expected_Points_round1'],2)) #X points total
    indices =  sorted(range(len(xPoints)), key = lambda sub: xPoints[sub])[-100:]
    indices = list(reversed(np.array(indices)))
    
    Names =  data_final['fpl_name'].to_list()

    TotPoints = [round(xPoints[i],1) for i in indices]
    Name = [Names[i] for i in indices]
    print(TotPoints)
    bank = session["bank"]
    return render_template('dashboard.html', name=current_user.username, Squad = Squad, Squad_Position = Squad_Position ,Squad_Team = Squad_Team, 
                                             Squad_xPoints = Squad_xPoints, Squad_Captain = Squad_Captain, buy_list1 = buy_list1, sell_list1 = sell_list1,
                                             squad_points = squad_points, TotPoints = TotPoints, Name=Name, point_increase = point_increase, zero_players = zero_players,
                                             zero_players_bench = zero_players_bench, rank = rank, n_transfers = n_transfers, bank = bank)

@app.route('/top100')
@login_required
def top100():
 
    xPointsTotal1 = list(data_final['Expected_Points_discounted']) #X points total
    xPoints = list(data_final['Expected_Points_round1']) #X points total
    cost_players = list(data_final['cost']/10) #X points total
    TotalPoints = list(np.array(xPointsTotal1))   
    xGrowth = list(np.array(xPoints)/np.array(data_final['cost']/10))
    indices =  sorted(range(len(xPoints)), key = lambda sub: xPoints[sub])[-100:]
    indices = list(reversed(np.array(indices)))
    
    Names =  data_final['fpl_name'].to_list()
    Teams =  data_final['team'].to_list()

    TotPoints = [round(TotalPoints[i],0) for i in indices]
    Name = [Names[i] for i in indices]
    Team1 = [team_lookup_num[Teams[i]] for i in indices]
    xPoints1 = [round(xPoints[i],1) for i in indices]
    xPointsTotal1 = [round(xPointsTotal1[i],0) for i in indices]
    Transfer1 = [0*i for i in indices]
    TotalPoints1  = [round(TotalPoints[i],1) for i in indices] 
    xGrowth1  = [round(xGrowth[i]*100,1) for i in indices]   
    cost_players1 = [round(cost_players[i],0) for i in indices] 

    return render_template('top100.html', TotPoints=TotPoints, Name = Name, Team1 = Team1 ,xPoints1 = xPoints1, Transfer1 = Transfer1,
                                                xPointsTotal1 = xPointsTotal1, TotalPoints1 = TotalPoints1, xGrowth1=xGrowth1, cost_players1=cost_players1, 
                                                current_round = current_round)

@app.route('/top100growth')
@login_required
def top100growth():

    xPointsTotal1 = list(data_final['Expected_Points_discounted']) #X points total
    xPoints = list(data_final['Expected_Points_round1']) #X points total
    cost_players = list(data_final['cost']/10) #X points total
    TotalPoints = list(np.array(xPointsTotal1))   
    xGrowth = list(np.array(xPoints)/np.array(data_final['cost']/10))
    indices =  sorted(range(len(xGrowth)), key = lambda sub: xGrowth[sub])[-100:]
    indices = list(reversed(np.array(indices)))
    
    Names =  data_final['fpl_name'].to_list()
    Teams =  data_final['team'].to_list()

    TotPoints = [round(TotalPoints[i],0) for i in indices]
    Name = [Names[i] for i in indices]
    Team1 = [team_lookup_num[Teams[i]] for i in indices]
    xPoints1 = [round(xPoints[i],0) for i in indices]
    xPointsTotal1 = [round(xPointsTotal1[i],0) for i in indices]
    Transfer1 = [0*i for i in indices]
    TotalPoints1  = [round(TotalPoints[i],0) for i in indices] 
    xGrowth1  = [round(xGrowth[i]*100,1) for i in indices]   
    cost_players1 = [round(cost_players[i],0) for i in indices] 

    return render_template('top100growth.html', TotPoints=TotPoints, Name = Name, Team1 = Team1 ,xPoints1 = xPoints1, Transfer1 = Transfer1,
                                                xPointsTotal1 = xPointsTotal1, TotalPoints1 = TotalPoints1, xGrowth1=xGrowth1, cost_players1=cost_players1, 
                                                current_round = current_round)

@app.route('/ExpectedCS', methods=['GET', 'POST'])
@login_required
def ExpectedCS():
    
    Team1 = list(fte_to_web_cs['6'])
    col1 = list(fte_to_web_cs['0'])
    col2 = list(fte_to_web_cs['1'])
    col3 = list(fte_to_web_cs['2'])
    col4 = list(fte_to_web_cs['3'])
    col5 = list(fte_to_web_cs['4'])
    col6 = list(fte_to_web_cs['5'])
    Avg = list(round(fte_to_web_cs[['0','1','2','3','4','5']].mean(axis=1),2) )
    Min = list(round(fte_to_web_cs[['0','1','2','3','4','5']].min(axis=1),2))
    Max = list(round(fte_to_web_cs[['0','1','2','3','4','5']].max(axis=1),2))  

    return render_template('ExpectedCS.html', Team1=Team1, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, 
                                            Avg=Avg,Min=Min, Max=Max, current_round = current_round)
                           
@app.route('/ExpectedG', methods=['GET', 'POST'])
@login_required
def ExpectedG():
    
    Team1 = list(fte_to_web_xg['6'])
    col1 = list(fte_to_web_xg['0'])
    col2 = list(fte_to_web_xg['1'])
    col3 = list(fte_to_web_xg['2'])
    col4 = list(fte_to_web_xg['3'])
    col5 = list(fte_to_web_xg['4'])
    col6 = list(fte_to_web_xg['5'])
    Avg = list(round(fte_to_web_xg[['0','1','2','3','4','5']].mean(axis=1),2) )
    Min = list(round(fte_to_web_xg[['0','1','2','3','4','5']].min(axis=1),2))
    Max = list(round(fte_to_web_xg[['0','1','2','3','4','5']].max(axis=1),2))  

    return render_template('ExpectedG.html', Team1=Team1, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, 
                                            Avg=Avg,Min=Min, Max=Max, current_round = current_round)

@app.route('/ExpectedW', methods=['GET', 'POST'])
@login_required
def ExpectedW():
    
    Team1 = list(fte_to_web_xw['6'])
    col1 = list(fte_to_web_xw['0'])
    col2 = list(fte_to_web_xw['1'])
    col3 = list(fte_to_web_xw['2'])
    col4 = list(fte_to_web_xw['3'])
    col5 = list(fte_to_web_xw['4'])
    col6 = list(fte_to_web_xw['5'])
    Avg = list(round(fte_to_web_xw[['0','1','2','3','4','5']].mean(axis=1),2))
    Min = list(round(fte_to_web_xw[['0','1','2','3','4','5']].min(axis=1),2))
    Max = list(round(fte_to_web_xw[['0','1','2','3','4','5']].max(axis=1),2))  

    return render_template('ExpectedW.html', Team1=Team1, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, 
                                            Avg=Avg,Min=Min, Max=Max, current_round = current_round)
                           
@app.route('/AnalyzePlayers', methods=['GET', 'POST'])
@login_required
def AnalyzePlayers():
    
    Player_stats_temp = Player_stats[Player_stats['round'].isin(range(current_round,current_round+6,1))]
    Names = Player_stats_temp['fpl_name'].unique()

    if request.method =='GET':
        
        Player1 = Names[1]
        Player2 = Names[2]

    else:
        Player1 = request.form.get("Player1")
        Player2= request.form.get("Player2")   
        
    form = Form()
    form.Player1.choices = [Player1, "---"] + sorted(list(Names))
    form.Player2.choices = [Player2, "---"] + sorted(list(Names))

    
    values1 = list(round(Player_stats_temp[Player_stats_temp['fpl_name'] == Player1]['Expected_Points'],2))
    values2 = list(round(Player_stats_temp[Player_stats_temp['fpl_name'] == Player2]['Expected_Points'],2))
    average = list(round(Player_stats_temp[['Expected_Points','round']].groupby(['round']).mean()['Expected_Points'],2))
    labels = ['1','2','3','4','5','6']
   
    
    Name1 = Player1
    Name2 = Player2
    
    print(Name1)
    
    print(Name2)
    print(values1)
    print(values2)
    print(average)
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
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)