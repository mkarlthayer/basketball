# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 08:26:20 2022

@author: kthay
"""

from sklearn.tree import DecisionTreeRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# get data from my github
df_2020 = pd.read_csv(r'https://raw.githubusercontent.com/mkarlthayer/basketball/main/2020_NBA_Contracts.csv')   #read the csv file (put 'r' before the path string to address any special characters in the path, such as '\'). Don't forget to put the file name at the end of the path + ".csv"
df_2021 = pd.read_csv(r'https://raw.githubusercontent.com/mkarlthayer/basketball/main/2021_NBA_Contracts.csv')
df_2022 = pd.read_csv(r'https://raw.githubusercontent.com/mkarlthayer/basketball/main/2022_NBA_Contracts.csv')

# combine last 3 years of contract data
df_combined = pd.concat([df_2020, df_2021, df_2022])

# use selected stats as predictor variable 
inputs = ['PTS','Age','PER']
X = df_combined[inputs]
# set y to avg_salary
y = df_combined[['Avg_Salary']]

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size = .75)
depth = 2
model = DecisionTreeRegressor(max_depth = depth, random_state=0)
model.fit(X_train,y_train)

# calculate r2 and adjusted r2
rsq = model.score(X_test, y_test)
print(f'R-squared: {rsq}')
adjusted_rsq = 1 - (1-model.score(X_test, y_test))*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)
print(f'Adjusted: {adjusted_rsq}')


max_depth_range = list(range(1, 25))
# List to store the average RMSE for each value of max_depth:
r2_list = []
for depth in max_depth_range:
    model = DecisionTreeRegressor(max_depth = depth,
                            random_state = 0)
    model.fit(X_train, y_train)   
    
    score = model.score(X_test, y_test)
    r2_list.append(score)

# graph of r2 data
fig, ax = plt.subplots(nrows = 1, ncols = 1,
                        figsize = (10,7),
                        facecolor = 'white');
ax.plot(max_depth_range,
        r2_list,
        lw=2,
        color='r')
ax.set_xlim([1, max(max_depth_range)])
ax.grid(True,
        axis = 'both',
        zorder = 0,
        linestyle = ':',
        color = 'k')
ax.tick_params(labelsize = 18)
ax.set_xlabel('max_depth', fontsize = 24)
ax.set_ylabel('R^2', fontsize = 24)
ax.set_title('Model Performance on Test Set', fontsize = 24)
fig.tight_layout()

