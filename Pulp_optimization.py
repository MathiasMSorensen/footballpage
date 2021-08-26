def Pulp_optimization(Teams, N, Data, TranferIn, TranferOut ,TotalPoints, \
                      Positions, ExcludePlayers, IncludePlayers, ExcludeTeam, \
                      cash, Names, xPoints, n_transfers, squad_old_index, \
                      sub_1_discount, sub_2_discount,sub_3_discount, sub_gk_discount, Budget_from_players):
    
    import pulp
    from pulp import lpSum
    import numpy as np
    import pandas as pd
    from dictionaries import team_lookup_num, team_lookup_num_reverse
    
    Output_list = []
    cost_squad_list = []
    nShare_list = []
    Budget_list = []

    ExcludeTeam_help = ExcludeTeam
    ExcludeTeam = []
    for i in range(len(ExcludeTeam_help)):
        ExcludeTeam.append(team_lookup_num_reverse[ExcludeTeam_help[i]])

    squad_old = list(np.where(Data['fpl_name'].isin(squad_old_index), 1, 0))
    TranferOut_pd = pd.DataFrame(TranferOut)
    Budget = Budget_from_players + cash

    for i in range(6):
        n_transfers = i
        # Set up model:
        model = pulp.LpProblem("Constrained_maximisation", pulp.LpMaximize)

        players = [
            pulp.LpVariable("z{}".format(i), lowBound=0, upBound=1, cat='Integer') for i in range(N)
        ]
        sub1 = [
            pulp.LpVariable("zzz{}".format(i), lowBound=0, upBound=1, cat='Integer') for i in range(N)
        ]
        sub2 = [
            pulp.LpVariable("zzzz{}".format(i), lowBound=0, upBound=1, cat='Integer') for i in range(N)
        ]
        sub3 = [
            pulp.LpVariable("zzzzz{}".format(i), lowBound=0, upBound=1, cat='Integer') for i in range(N)
        ]
        subs_gk = [
            pulp.LpVariable("xx{}".format(i), lowBound=0, upBound=1, cat='Integer') for i in range(N)
        ]
        captain = [
            pulp.LpVariable("y{}".format(i), lowBound=0, upBound=1, cat='Integer') for i in range(N)
        ]
        y_help = [
            pulp.LpVariable("yy{}".format(i), lowBound=0, upBound=1, cat='Integer') for i in range(N)
        ]

        # Objective function:
        model += lpSum((captain[i] + players[i]) * TotalPoints[i] + \
                        (sub1[i]) * TotalPoints[i] * sub_1_discount + \
                        (sub2[i]) * TotalPoints[i] * sub_2_discount + \
                        (sub3[i]) * TotalPoints[i] * sub_3_discount + \
                        (subs_gk[i]) * TotalPoints[i] * sub_gk_discount  for i in range(N))
                    
        # Team constraint
        model += lpSum(players[i] for i in range(N)) == 11
        model += lpSum(sub1[i] for i in range(N)) == 1
        model += lpSum(sub2[i] for i in range(N)) == 1
        model += lpSum(sub3[i] for i in range(N)) == 1
        model += lpSum(subs_gk[i] for i in range(N)) == 1

        # Cost constraint
        model += lpSum((players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) * TranferIn[i] for i in range(N)) <= Budget

        # Position constraints on squad
        model += lpSum((players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) for i in range(N) if Positions[i] == 'Goalkeeper') == 2
        model += lpSum((players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) for i in range(N) if Positions[i] == 'Defense') == 5
        model += lpSum((players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) for i in range(N) if Positions[i] == 'Midfield') == 5
        model += lpSum((players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) for i in range(N) if Positions[i] == 'Striker') == 3

        # Position constraints on players
        model += lpSum(players[i] for i in range(N) if Positions[i] == 'Goalkeeper') == 1
        model += lpSum(players[i] for i in range(N) if Positions[i] == 'Defense') >= 3
        model += lpSum(players[i] for i in range(N) if Positions[i] == 'Defense') <= 5
        model += lpSum(players[i] for i in range(N) if Positions[i] == 'Midfield') >= 3
        model += lpSum(players[i] for i in range(N) if Positions[i] == 'Midfield') <= 5
        model += lpSum(players[i] for i in range(N) if Positions[i] == 'Striker') >= 1
        model += lpSum(players[i] for i in range(N) if Positions[i] == 'Striker') <= 3  

        # Position constraints on subs
        model += lpSum((sub1[i] + sub2[i] + sub3[i]) for i in range(N) if Positions[i] == 'Goalkeeper') == 0
        model += lpSum(sub1[i] for i in range(N) if Positions[i] == 'Defense') == 1
        model += lpSum(subs_gk[i] for i in range(N) if Positions[i] == 'Goalkeeper') == 1

        # Club constraint
        for team in np.unique(Teams):
            model += lpSum(players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i] for i in range(N) if Teams[i] == team) <= 3

        # Captain constraint
        model += lpSum(captain[i] for i in range(N)) == 1

        for i in range(N):  
            model += (players[i] - captain[i]) >= 0
                        
        # # You can only be player | sub | sub_gk
        # for i in range(N):  
            model += (players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) <= 1

        # # help matrix
        # for i in range(N):  
            model += (y_help[i]-(players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i])) <= 0

        # for i in range(N):  
            model += (y_help[i]-squad_old[i]) <= 0

        # for i in range(N):  
            model += (y_help[i] - squad_old[i] - (players[i] + sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) + 1 >= 0)

        # Include players
        # for i in range(N):
            if Names[i] in IncludePlayers:
                model += (players[i] +  sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) == 1
            
        # Exclude players
        # for i in range(N):
            if Names[i] in ExcludePlayers:
                model += (players[i] +  sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) == 0

        # Exclude teams
        # for i in range(N):
            if Teams[i] in ExcludeTeam:
                model += (players[i] +  sub1[i] + sub2[i] + sub3[i] + subs_gk[i]) == 0 

        # transfer_coinstraint
        model += lpSum(y_help[i] for i in range(N)) == 15 - n_transfers


        # Solve problem:
        print(Budget)
        if model.solve()==1:
            print("all good")
            
            Output = []
            for i in range(N):
                if ((players[i].value()==1) & (squad_old[i] == 0)):
                    Output.append([Names[i], team_lookup_num[Teams[i]], Positions[i], int(TotalPoints[i]), int(xPoints[i]), int(TranferIn[i]),'player','New',''])
                elif ((players[i].value()==1) & (squad_old[i] != 0)):
                    Output.append([Names[i], team_lookup_num[Teams[i]], Positions[i], int(TotalPoints[i]), int(xPoints[i]), int(TranferIn[i]),'player','',''])
                elif ((sub1[i].value() + sub2[i].value() + sub3[i].value() + subs_gk[i].value()==1) & (squad_old[i] == 0)):
                    Output.append([Names[i], team_lookup_num[Teams[i]], Positions[i], int(TotalPoints[i]), int(xPoints[i]), int(TranferIn[i]),'sub','New',''])
                elif ((sub1[i].value() + sub2[i].value() + sub3[i].value() + subs_gk[i].value()==1) & (squad_old[i] != 0)):
                    Output.append([Names[i], team_lookup_num[Teams[i]], Positions[i], int(TotalPoints[i]), int(xPoints[i]), int(TranferIn[i]),'sub','',''])
            
            Output = pd.DataFrame(Output)
            Output.columns = ['Names','Teams','Positions','xPoints','TotalPoints','Cost','player_sub','new_old','Captain']
            Output = Output.sort_values(['player_sub','Positions']).reset_index(drop = True)
            Output = pd.concat([Output[((Output['Positions']=='Goalkeeper') & (Output['player_sub']=='player'))].reset_index(drop = True),
                                Output[((Output['Positions']!='Goalkeeper') | (Output['player_sub']!='player'))].reset_index(drop = True)]).reset_index(drop = True)
            
            Output['Captain'][Output['TotalPoints'].idxmax()] = 'Captain'

            cost_squad = 0
            for i in range(N):
                if (players[i].value() + sub1[i].value() + sub2[i].value() + sub3[i].value() + subs_gk[i].value()) != 0 :
                    cost_squad = TranferIn[i] + cost_squad
                
            nShare = cost_squad/Budget*100

        else:
            print("Wrong")
            Output = 0
            cost_squad = 0
            nShare = 0

        Output_list.append(Output)
        cost_squad_list.append(cost_squad)
        nShare_list.append(nShare)
        Budget_list.append(Budget)

    return Output_list, cost_squad_list, nShare_list, Budget_list
  

