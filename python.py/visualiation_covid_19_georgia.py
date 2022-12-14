# -*- coding: utf-8 -*-
"""Visualiation-Covid-19-Georgia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FojtHqXGxxp67yYPZHsV5zG31EzRxj1X

# Step 1: Loading in Packages
"""

# the below packages are related to loading and performing basic
# transformation of data

import pandas as pd
import numpy as np
import seaborn 

print ('cell succesfully ran')

# now we are going to load in some packages that help with visualization of data

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sns.set_theme(style='whitegrid')
print ('cell succesfully run')

"""# Loading in data"""

dataframe = pd.read_csv('https://raw.githubusercontent.com/nori0227/AHI_Microcourse_Visualization-HHA-507-MICROCOURSE/main/Data/Georgia_COVID/Georgia_COVID-19_Case_Data.csv')

dataframe

len (dataframe)

dataframe.shape

"""# Describing the variables"""

dataframe.info()

list(dataframe)

dataframe['COUNTY'].value_counts() ## number of times found in a row ##

dataframe_counties = dataframe['COUNTY'].value_counts()
dataframe_counties.head(5) ###look at certain rows##

"""# Transforming columns"""

dataframe['DATESTAMP']

## creating a copy of the existing column so that we keep the original column
## can override the column if needed, but because we are unsure
## where we are going to take the analysis - lets keep the original datestamp column

dataframe['DATESTAMP_MOD'] = dataframe['DATESTAMP']
print (dataframe['DATESTAMP_MOD'].head(10))
print (dataframe['DATESTAMP_MOD'].dtypes)

dataframe ## there is a new column 'DATESTAMP_MOD' on the right side of the table

dataframe['DATESTAMP_MOD'] = pd.to_datetime(dataframe['DATESTAMP_MOD']) # this function --pd.to_datetime-- classify to datetime instead of plain object
dataframe['DATESTAMP_MOD'].dtypes # check the dtypes

dataframe[['DATESTAMP', 'DATESTAMP_MOD']] # to compare how the new function 'DATESTAMP_MOD' looks in comparison to the original column 'DATESTAMP'
# new column, DATESTAMP_MOD is no longer a string, but a timestamp

dataframe['DATESTAMP_MOD_DAY'] = dataframe['DATESTAMP_MOD'].dt.date  # --- .dt.date ----extract the date only 
dataframe['DATESTAMP_MOD_DAY'] # outputted dates only

dataframe['DATESTAMP_MOD_Year'] = dataframe['DATESTAMP_MOD'].dt.year
dataframe['DATESTAMP_MOD_Year']

dataframe['DATESTAMP_MOD_Month'] = dataframe['DATESTAMP_MOD'].dt.month
dataframe['DATESTAMP_MOD_Month']
dataframe

# combine month and year
dataframe['DATESTAMP_MOD_Month_Year'] = dataframe['DATESTAMP_MOD'].dt.to_period('M')
dataframe['DATESTAMP_MOD_Month_Year'].sort_values()

dataframe['DATESTAMP_MOD_WEEK'] = dataframe['DATESTAMP_MOD'].dt.week
dataframe['DATESTAMP_MOD_WEEK']

dataframe['DATESTAMP_MOD_QUARTER'] = dataframe['DATESTAMP_MOD'].dt.to_period(
    'Q')
dataframe['DATESTAMP_MOD_QUARTER']
dataframe['DATESTAMP_MOD_QUARTER'].sort_values()

dataframe['DATESTAMP_MOD_DAY_STRING'] = dataframe['DATESTAMP_MOD_DAY'].astype(str)

dataframe['DATESTAMP_MOD_WEEK_STRING'] = dataframe['DATESTAMP_MOD_WEEK'].astype(str)
dataframe['DATETIME_STRING'] = dataframe['DATESTAMP_MOD_Month_Year'].astype(
    str)

dataframe

"""## Getting the counties required for our analysis

### we know that the counties we want to analyze are:
- Gob
- Dekalb
- Fulton
- Gwinnett
- Hall
"""

dataframe['COUNTY']

countList = ['COBB', 'DEKALB', 'FULTON', 'GWINNETT', 'HALL'] # creating a list of counties that we care about
countList

selectCounties = dataframe[dataframe['COUNTY'].isin(countList)] #creating a subset of dataframe with list of selected counties only
len(selectCounties) #provides number of rows in new dataframe
selectCounties

"""# Getting just the specific date/time frame we want

#### 'dataframe' = length ~90,000
#### 'selectCounties' = length 2,830
#### 'selectCountyTime' = ???/TBD
"""

selectCountyTime = selectCounties

selectCountyTime['DATESTAMP_MOD_Month_Year']

selectCountyTime_april2020 = selectCountyTime[selectCountyTime['DATESTAMP_MOD_Month_Year'] == '2020-04'] ### looking for just a subset of our data that only contains the five counties for the month of April
len(selectCountyTime_april2020) ## contains a 150 rows for this five county only for the month of April

selectCountyTime_aprilmay2020 = selectCountyTime[(selectCountyTime['DATESTAMP_MOD_Month_Year'] == '2020-05') | (selectCountyTime['DATESTAMP_MOD_Month_Year'] == '2020-04')]
len(selectCountyTime_aprilmay2020)

selectCountyTime_aprilmay2020.head(50)

"""# Creating the final dataframe / specific columns-features-attributes- that we care about"""

finalDF = selectCountyTime_aprilmay2020[[
    'COUNTY',
    'DATESTAMP_MOD',
    'DATESTAMP_MOD_DAY',
    'DATESTAMP_MOD_DAY_STRING',
    'DATETIME_STRING',
    'DATESTAMP_MOD_Month_Year',
    'C_New',  # cases - new
    'C_Cum',  # cases - total
    'H_New',  # hospitalizations - new
    'H_Cum',  # hospitalizations - total
    'D_New',  # deaths - new
    'D_Cum',  # deaths-total
]]
finalDF

"""# Looking at total covid cases by month"""

finalDF_dropdups = finalDF.drop_duplicates(
    subset=['COUNTY', 'DATETIME_STRING'], keep='last')
finalDF_dropdups

pd.pivot_table(finalDF_dropdups, values='C_Cum', index=['COUNTY'],
               columns=['DATESTAMP_MOD_Month_Year'], aggfunc=np.sum)

vis1 = sns.barplot(x='DATESTAMP_MOD_Month_Year',
                   y='C_Cum', data=finalDF_dropdups)

vis2 = sns.barplot(x='DATESTAMP_MOD_Month_Year', y='C_Cum',
                   hue ='COUNTY', data=finalDF_dropdups)

plotlyl = px.bar(finalDF_dropdups, x='DATETIME_STRING',
                 y='C_Cum', color='COUNTY', barmode='group')
plotlyl.show()

plotly2 = px.bar(finalDF_dropdups, x='DATETIME_STRING',
                 y='C_Cum', color='COUNTY', barmode='stack')
plotly2.show()

"""# Looking at total covid cases by DAY"""

daily = finalDF
daily
len(daily)

pd.pivot_table(daily, values='C_Cum', index=['COUNTY'],
               columns=['DATESTAMP_MOD_DAY'], aggfunc=np.sum)

# inverting the rows and columns
tempdf = pd.pivot_table(daily, values='C_Cum', index=['DATESTAMP_MOD_DAY'],
               columns=['COUNTY'], aggfunc=np.sum)
tempdf.head(100)

startdate = pd.to_datetime('2020-04-26').date()
enddate = pd.to_datetime('2020-05-09').date()

maskFilter = (daily['DATESTAMP_MOD_DAY'] >= startdate) & (
    daily['DATESTAMP_MOD_DAY'] <= enddate)
dailySpecific = daily.loc[maskFilter]
dailySpecific

dailySpecific[dailySpecific['COUNTY'] == 'FULTON']

vis3 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum')

vis3 = sns.lineplot(data=dailySpecific,
                    x='DATESTAMP_MOD_DAY', y='C_Cum', hue='COUNTY')

plotly3 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY',
                 y='C_Cum', color='COUNTY')
plotly3.show()

plotly4 = px.bar(dailySpecific,
                 x='DATESTAMP_MOD_DAY',
                 y='H_New',
                 color='COUNTY',
                 barmode='group')
plotly4.show()

plotly4 = px.bar(dailySpecific,
                 x='DATESTAMP_MOD_DAY',
                 y='H_Cum',
                 color='COUNTY',
                 barmode='group')
plotly4.show()

dailySpecific['newHospandDeathCovid'] = dailySpecific['D_New'].astype(
    int) + dailySpecific['H_New'].astype(int) + dailySpecific['C_New'].astype(int)
dailySpecific['newHospandDeathCovid']

dailySpecific['newHospandDeath'] = dailySpecific['D_New'].astype(
    int) + dailySpecific['H_New'].astype(int)
dailySpecific['newHospandDeath']
dailySpecific

plotly8 = px.bar(dailySpecific,
                 x='DATESTAMP_MOD_DAY',
                 y='newHospandDeathCovid',
                 color='COUNTY',
                 title='Georgia 2020 COVID Data: New Hospitalizations, Deaths, and COVID cases by County',
                 labels={
                     'DATESTAMP_MOD_DAY': "Time (Month, Day, Year)",
                     'newHospandDeathCovid': "Total Count"
                 },
                 barmode='group')

plotly8.update_layout(
    xaxis=dict(
        tickmode='linear',
        type='category'
    )
)
plotly8.show()