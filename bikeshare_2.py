import time
import pandas as pd
import numpy as np
import calendar
from datetime import timedelta #using timedelta to show the user how else seconds can be represented


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


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    correct_input = False #this will be used to confirm with the user that they have selected the city that they want.
    while correct_input == False:
        valid_input = False #this variable will keep the while loop running until the user enters valid inputs
        while valid_input == False:
            print('Please select the city that you would like to explore.')
            print('Make your selection by entering the letter that corresponds to your city of choice (indicated by the brackets).')
            selection = input('Please choose between [C]hicago, [N]ew York City, and [W]ashington DC: ').title()
            if selection == 'C':
                city = 'chicago'
                valid_input = True
            elif selection == 'N':
                city = 'new york city'
                valid_input = True
            elif selection == 'W':
                city = 'washington'
                valid_input = True
            else: invalid_input()
        print('Thank you for making your selection.')
        valid_input = False
        while valid_input == False: #checks with the user to double-check that they made they right selection
            print('You have selected {}.'.format(city.title()))
            is_correct = input('Is this correct? [Y]es or [N]o: ').title()
            if is_correct == 'Y':
                correct_input = True
                valid_input = True
            elif is_correct == 'N':
                valid_input = True
            else: invalid_input()
    print('\nExcellent. Thank you for making your selection.\n')

    # get user input for month (all, january, february, ... , june)
    correct_input = False
    print('Okay, now we need to know what month you\'re looking to filter for.')
    while correct_input == False:
        valid_input = False
        while valid_input == False:
            integer_input = False #This variable is used to keep track of whether the user has input an integer
            while integer_input == False:
                try:
                    print('For what month would you like to filter? Please enter a number that corresponds to your month of choice.')
                    print('1 for January, 2 for February, etc. Please enter 0 if you would like to select all months.')
                    month = int(input('Please enter your selection here: '))
                    integer_input = True
                except:
                    invalid_input()
            if month >= 0 and month <= 12:
                print('Thank you for making your selection')
                valid_input = True
            else:
                invalid_input()
        valid_input = False
        while valid_input == False: #checks with the user to see if the month that they selected is the one that they want
            if month != 0:
                print('You have selected {} ({})'.format(month, calendar.month_name[month]))
            else: print('You have seleced 0 (All months).')
            is_correct = input('Is this correct? [Y]es or [N]o: ').title()
            if is_correct == 'Y':
                correct_input = True
                valid_input = True
            elif is_correct == 'N':
                valid_input = True
            else: invalid_input()
    print('\nExcellent. Thank you for making your selection.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Okay, now we need to know what day of the week you\'re looking to filter for.')
    correct_input = False
    while correct_input == False:
        valid_input = False
        while valid_input == False:
            integer_input = False #This variable is used to keep track of whether the user has input an integer
            while integer_input == False:
                try:
                    print('For what day of the week would you like to filter? Please enter a number that corresponds to your day of choice.')
                    print('1 for Monday, 2 for Tuesday, etc. Please enter 0 if you would like to select all days of the week.')
                    day = int(input('Please enter your selection here: '))
                    integer_input = True
                except:
                    invalid_input()
            if day >= 0 and day <= 7:
                print('Thank you for making your selection')
                valid_input = True
            else:
                invalid_input()
        valid_input = False
        while valid_input == False: #checks with the user to make sure that they made the input that they wanted
            if day != 0:
                print('You have selected {} ({}).'.format(day, calendar.day_name[day-1]))
            else: print('You have selected 0 (All days).')
            is_correct = input('Is this correct? [Y]es or [N]o: ').title()
            if is_correct == 'Y':
                correct_input = True
                valid_input = True
            elif is_correct == 'N':
                valid_input = True
            else: invalid_input()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load the main csv file
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #filter by month, if applicable
    if month != 0:
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter by day, if applicable
    if day != 0:
        # filter by day to create the new DataFrame
        df = df[df['day_of_week'] == calendar.day_name[day-1]]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
    The filtered dataframe, df, is passed in, along with the user's selection
    of month and day, to help with determining what statistics are shown"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, if not being filtered for one particular month
    if month == 0:
        print('The most popular month for travel, per your filter, is {}.'.format(calendar.month_name[int(df['month'].mode().values)]))
    else: print('You have elected to filter by a single month, so we will not calculate the most popular month.')

    # display the most common day of week, if not being filtered for one particular day of week
    if day == 0:
        print('The most popular day for travel, per your filter, is {}.'.format(df['day_of_week'].mode().values[0]))
    else: print('You have elected to filter by a single day, so we will not calculate the most popular day of the week.')

    # display the most common start hour
    popular_hour = int(df['hour'].mode().values)
    print('The most frequent start hour, per your filter, is', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    df dataframe containing the user's filtered data is passed in.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most popular start station, per your filter, is {}.'.format(df['Start Station'].mode().values[0]))

    # display most commonly used end station
    print('The most popular end station, per your filter, is {}.'.format(df['End Station'].mode().values[0]))

    # display most frequent combination of start station and end station trip
    routes_sorted = df.groupby(['Start Station'])['End Station'].value_counts()
    top_route = routes_sorted.nlargest(1).index[0]
    print('The most frequent trip, per your filter, was from {} to {}, for a total of {} trips.'.format(top_route[0], top_route[1], routes_sorted.max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #print(df.head())
    total_trip = df['Trip Duration'].sum()
    print('The total travel time for all users, per your filter, was {} seconds.'.format(total_trip))
    #print('This equates to {} '.format(timedelta(0, total_trip)))

    # display mean travel time
    avg_trip = df['Trip Duration'].mean()
    print('The average travel time, per your filter, was {} seconds.'.format(avg_trip))
    print('This equates to {} '.format(timedelta(0, avg_trip)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Here are how many of each user type there are, per your filter:')
    print(df['User Type'].value_counts(),'\n')

    # Display counts of gender
    if city != 'washington':
        df['Gender'].fillna('Unspecified', inplace=True)
        print('Here are how many of each gender there are, per your filter:')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
        print('\nThe earliest year of birth, per your filter, is {}.'.format(int(df['Birth Year'].min())))
        print('The most recent year of birth, per your filter, is {}.'.format(int(df['Birth Year'].max())))
        print('The most common year of birth, per your filter, is {}.'.format(int(df['Birth Year'].mode())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    This asks the user if they would like to view the raw data for the DataFrame
    that is passed.

    Args:
    df: DataFrame.  This is the input DataFrame
    """

    valid_input = False #this variable will keep the while loop running until the user enters valid inputs
    while valid_input == False:
        print('Would you like to see the raw data?')
        selection = input('[Y]es or [N]o: ').title()
        if selection == 'Y' or selection == 'N':
            valid_input = True
        else: invalid_input()
    print('Thank you for making your selection.')

    if selection == 'Y':
        continue_display = True
        display_counter = 0
    else: continue_display = False

    while continue_display == True: #this loop will continue to display the raw data, 5 items at a time, until such time that the user decides that they don't want to continue.
        try:  #This will hopefully kick the user out of the while loop and continue with the program if the for loop below start to go out of bounds
            for i in range(display_counter, display_counter+5):
                print(df.iloc[i])
            valid_input = False #this variable will keep the while loop running until the user enters valid inputs
            while valid_input == False:
                print('\nWould you like to continue viewing the raw data?')
                selection = input('[Y]es or [N]o: ').title()
                if selection == 'Y' or selection == 'N':
                    valid_input = True
                else: invalid_input()
            if selection == 'Y':
                display_counter += 5
            else: continue_display = False
        except:
            print('It looks like this thing has gone as far as it\'s going to go.')
            continue_display = False

def main():
    while True:
        #clear the screen
        print("\033[H\033[J")

        #this gets the data from the user
        city, month, day = get_filters()

        #this gets the DataFrame per the user's filter paramenters
        df = load_data(city, month, day)

        if df.empty == False: #this checks to make sure that the DataFrame isn't empty
            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            raw_data(df)
        else: print('Unfortunately, your filter did not return any results.\n')

        #see if the user wants to start over
        valid_input = False #this variable will keep the while loop running until the user enters valid inputs
        while valid_input == False:
            print('Would you like to restart?')
            restart = input('[Y]es or [N]o: ').title()
            if restart == 'Y' or restart == 'N':
                valid_input = True
            else: invalid_input()
        if restart == 'N':
            print('Thank you for taking the time to use this program.')
            print('Have a nice day.  Goodbye.')
            break


#this checks to make sure that this script is being run as the main program
if __name__ == "__main__":
	main()
