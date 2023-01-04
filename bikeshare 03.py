import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
# an empty variable was initiated
    city = ''
    # looping out to check weather city entered is available or not
    while city not in CITY_DATA.keys():
        print("Please choose a city by typing the name of the following cities, chicago, new york city or washington:")
        print("\n1. Chicago 2. New York City 3. Washington")
        #converting the typed city name to lower case
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nPlease make sure you input the correct city name.")
            print("\nRestarting...")

    print(f"\nYou selected {city.title()} as your exploring city.")

    #prompting the user to input the month
    MONTH_DATA = {'all': 1, 'january': 2, 'february': 3, 'march': 4, 'april': 5, 'may': 6, 'june': 7 }
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease select a month from the following as your exploring month , january, february, march, april, may or june:")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nThe selection you've made is not correct, please select different month as per the following, january, february, march, april, may or june.")
            print("\nRestarting...")

    print(f"\nYou selected {month.title()} as your month to explore.")

    #constructing a list of all possible names of days for the user to select
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease select a day in the week as your exploring day by typing the day name :")
        # converting user input to lower case
        day = input().lower()

        if day not in DAY_LIST:
            print("\nhe selection you've made is not correct, please select different day as per the following, sunday, monday, tuesday, wednesday, thursday or friday.")
            print("\nRestarting...")

    print(f"\nYou selected  {day.title()} as your exploring day.")
    print(f"\nYou selected to show : {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*80)
    #Returning the selected titles
    return city, month, day

#loading .csv files function
def load_data(city, month, day):
    """
    Loads data for the specified city and applies filters by month and day.
    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or "all" to apply no month filter
        param3 (str): name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    #Load the city data from csv file
    print("\nDATA IS BEING RETREIVED...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert start and end time to the propper formate in a new column
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filtering by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #New dataframe for filtering by month
        df = df[df['month'] == month]

    #Filtering by day
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Returning the dataframe as per the selection
    return df

#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displaying statistics of the most frequent times of travel.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Utilizing the 'mode' to extract most favorable month for travel
    popular_month = df['month'].mode()[0]

    print(f"Most Popular Month (1 = January,2= February, 3= March, 4= April, 5= May,6 = June): {popular_month}")

    #Utilizing the 'mode' to extract most favorable day for travel
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nMost Popular Day: {popular_day}")

    #Converting hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    ##Utilizing the 'mode' to extract most favorable hour for travel
    popular_hour = df['hour'].mode()[0]

    print(f"\nMost Popular Start Hour: {popular_hour}")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    ##Utilizing the 'mode' to extract most favorable station to start travel
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most commonly used start station: {common_start_station}")

    ##Utilizing the 'mode' to extract most favorable station to end travel
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station: {common_end_station}")

    #Uses str.cat to combine two columsn in the df
    #Assigns the result to a new column 'Start To End'
    #Uses mode on this new column to find out the most common combination
    #of start and end stations
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combo}.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function for trip duration calculation
def trip_duration_stats(df):
    """Displays statistics on the average trip duration.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Utilizing sum method to calculate trip duration
    total_duration = df['Trip Duration'].sum()
    #Converting trip duration to minutes and seconds formate
    minute, second = divmod(total_duration, 60)
    #converting trip duration to hours formate
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    #Utilizing the mean method to calculate the average trip durations
    average_duration = round(df['Trip Duration'].mean())
    #Converting average trips durations in minute and seconds formate
    mins, sec = divmod(average_duration, 60)
    #Filtering and printing the average durations in hours, minutes and seconds
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating User Statistics...\n')
    start_time = time.time()
    #Utilizing the count method to count total number of users
    user_type = df['User Type'].value_counts()

    print(f"The types of users by number are given below:\n\n{user_type}")
 #This try clause is implemented to display the numebr of users by Gender
    #However, not every df may have the Gender column, hence this...
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Try clause to show only birth year and  most recent and common birth years
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to display the data frame itself as per user request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
     #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")

        rdata = input().lower()
        #Raw data to be displayed of user input yes
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease Ensure You Enter A Propper Response.")
            print("Your Response Is Not Within The Accepted Responses.")
            print("\nRestarting...\n")
    #A while loop here to prompt the user if he wishes to continue exploring the data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 10
        rdata = input().lower()
        #If user wishes to continue exploring data, this will continue to show 5 more rows of data
        if rdata == "yes":
             print(df[counter:counter+10])
        elif rdata != "yes":
             break

    print('-'*80)

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for using our exploring application")
            break

if __name__ == "__main__":
	main()
