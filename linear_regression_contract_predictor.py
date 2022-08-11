# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:44:55 2022

@author: kthay
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# get data from my github
df_2020 = pd.read_csv(r'https://raw.githubusercontent.com/mkarlthayer/basketball/main/2020_NBA_Contracts.csv')   #read the csv file (put 'r' before the path string to address any special characters in the path, such as '\'). Don't forget to put the file name at the end of the path + ".csv"
df_2021 = pd.read_csv(r'https://raw.githubusercontent.com/mkarlthayer/basketball/main/2021_NBA_Contracts.csv')
df_2022 = pd.read_csv(r'https://raw.githubusercontent.com/mkarlthayer/basketball/main/2022_NBA_Contracts.csv')

# combine last 3 years of contract data
df_combined = pd.concat([df_2020, df_2021, df_2022])

# use selected stats as predictor variable 
inputs = ['PTS','AST','TRB','BLK', 'eFG.','Age', 'GS', 'VORP']
X = df_combined[inputs]
# set y to avg_salary
y = df_combined[['Avg_Salary']]

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size = .75)
model = LinearRegression()
model.fit(X_train,y_train)
# calculate R sq and adjusted R sq
sal_rsq = model.score(X_test, y_test)
print(f'R-squared: {sal_rsq}')
sal_adjusted_rsq = 1 - (1-model.score(X_test, y_test))*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)
print(f'Adjusted: {sal_adjusted_rsq}')

# Repeat for years
y = df_combined[['Years']]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size = .75)
yrmodel = LinearRegression()
yrmodel.fit(X_train,y_train)

# Input player to predict salary
predictPlayer = input("Enter player name (first and last): ")
playerStats = df_2022.loc[df_2022["Player"] == predictPlayer]
print(playerStats[inputs])

predictedSal = model.predict(playerStats[inputs])
predictedSal = predictedSal.round(2)
predictedYrs = yrmodel.predict(playerStats[inputs])
predictedYrs = predictedYrs.round(1)

print(f'Predicted Salary: {predictedSal[0,0]}')
print(f"Actual Salary: {playerStats['Avg_Salary']}")
print(f'Predicted Years: {predictedYrs[0,0]}')
print(f"Actual Years: {playerStats['Years']}")

#print(model.intercept_)
#print(model.coef_)