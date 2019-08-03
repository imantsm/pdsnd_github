#fix for loop that displays raw data such that it maxes out at with how many entries there are
import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def invalid_input():
    """
    This function simply prints a boilerplate error message if the user
    inputs an invalid input. Through using this function, then only this function
    here has to be changed if one were to want change the behavior after invalid inputs
    is entered
    """
    print('\nOur apologies. That was not a valid input. Please try again.\n')

df = pd.read_csv('chicago.csv')
df['Start Time'] = pd.to_datetime(df['Start Time'])
df['End Time'] = pd.to_datetime(df['End Time'])

# extract month and day of week from Start Time to create new columns
df['month'] = df['Start Time'].dt.month
df['day_of_week'] = df['Start Time'].dt.weekday_name

print(df.head())

print('The most popular month for travel is {}'.format(calendar.month_name[df['month'].mode()[0]]))
print(df.iloc[0])
