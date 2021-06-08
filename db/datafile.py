import pandas as pd
import os

module_path = os.path.dirname(os.path.abspath('__file__')) + '/db'
Data = pd.read_excel(f'{module_path}/Model_v5.xlsx', 'Python')
Data_ECS = pd.read_excel(f'{module_path}/Model_v5.xlsx', 'Expected Clean Sheets')
Data_EG = pd.read_excel(f'{module_path}/Model_v5.xlsx', 'Expected Goals')
Data_EW = pd.read_excel(f'{module_path}/Model_v5.xlsx', 'Expected Wins')

# Create lists with variables:
Data = Data.dropna()

N = len(Data)
Names = list(Data['Name'])
Teams = list(Data['Team'])
Value = list(Data['Value'])
Positions = list(Data['Position'])
xPoints = list(Data['xPoints 1'])  # X points1
xPoints2 = list(Data['xPoints 2'])  # X points2
xPoints3 = list(Data['xPoints 3'])  # X points3
xPoints4 = list(Data['xPoints 4'])  # X points4
xPoints5 = list(Data['xPoints 5'])  # X points5
xPoints6 = list(Data['xPoints 6'])  # X points6
xPointsTotal = list(Data['xPoints Total'])  # X points total
TotalPoints = list(Data['Total'])  # Total x points-transfer
Transfer = list(Data['Transfer'])  # Value*0,01
Cost = list(Data['Cost'])  # Value+transfer
xGrowth = list(Data['xGrowth'])  # xGrowth
