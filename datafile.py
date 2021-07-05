import pandas as pd
import os 

APP_ROOT = os.path.dirname(os.path.abspath('__file__'))
Data = pd.read_excel(os.path.join(APP_ROOT, 'Model_v6.xlsx'), 'Python')
Data_names = pd.read_csv(os.path.join(APP_ROOT, 'holdet2.csv'))
Data_ECS = pd.read_excel(os.path.join(APP_ROOT, 'Model_v6.xlsx'), 'Expected Clean Sheets')
Data_EG = pd.read_excel(os.path.join(APP_ROOT, 'Model_v6.xlsx'), 'Expected Goals')
Data_EW = pd.read_excel(os.path.join(APP_ROOT, 'Model_v6.xlsx'), 'Expected Wins')

# Create lists with variables:
Data = Data.dropna()

N = len(Data)
Names = list(Data['Name'])
Names2 = list(Data_names['player'])
Teams = list(Data['Team'])
Value = list(Data['Value'])
Positions = list(Data['Position'])
xPoints = list(Data['xPoints 1']) #X points1
xPoints2 = list(Data['xPoints 2']) #X points2
xPoints3 = list(Data['xPoints 3']) #X points3
xPoints4 = list(Data['1/8 Finals']) #X points4
xPoints5 = list(Data['Quarter Finals']) #X points5
xPoints6 = list(Data['Semi Finals']) #X points6
xPoints7 = list(Data['Finals']) #X points6
xPointsTotal = list(Data['xPoints Total']) #X points total
TotalPoints = list(Data['Total']) # Total x points-transfer
Transfer = list(Data['Transfer']) #Value*0,01 
Cost = list(Data['Cost']) # Value+transfer
xGrowth = list(Data['xGrowth']) # xGrowth
N = len(Data)
Names = list(Data['Name'])
TotalPoints = list(Data['Total'])
Cost = list(Data['Cost'])
Positions = list(Data['Position'])
Teams = list(Data['Team'])
xPoints = list(Data['xPoints 1'])
Transfer = list(Data['Transfer'])