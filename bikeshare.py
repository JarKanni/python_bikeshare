import time
import calendar
import pandas as pd
import numpy as np

#list of cities and corresponding files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

#list of months covered in data including 'all' option
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']     

#list of days of week including 'all' option as index 0 so Monday returns 1
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']        

#establish blank variables
city = None
month = None
day = None


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #greets user upon start up, letting them know what the progam's all about
    print('Greetings and welcome!\nLet\'s explore US bikeshare data from the first half of 2017!\n')

    # get user input for city (all, chicago, new york city, washington).
    while True:
        city = str(input("Please choose a city (Chicago, New York City, Washington, or all): ")).lower()
        if city == 'all':
            #prints if user selects all cities
            print("\nThank you!  You chose to run all the data at once.  Wow, that's a lot!\n")
            break
        else:
            #prints selected city
            if city in CITY_DATA:
                print(f"\nThank you! You chose: {city.title()}\n")
                break
            else:
                print("Oops! Not a valid city.  Please try again...")
        

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Please choose a month from January to June: ")).lower()
        if month == 'all':
            #prints if user selects all months
            print("\nThank you! You chose all the months together. Quite a few days of data!\n")
            break
        else:
            if month in MONTHS:
                #prints selected month
                print(f"\nThank you! You chose: {month.title()}\n")
                break
            else:
                print("Shucks! Not a valid month between January to June.  Please try again...")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("Please choose a day of the week: ")).lower()
        if day == 'all':
            #prints if user selects all days
            print("\nThank you! You chose every single day of the week. Lots of data coming your way!\n")
            break
        else:
            if day in DAYS:
                #prints selected day
                print(f"\nThank you! You chose: {day.title()}\n")
                break
            else:
                print("Uh oh! Not a valid day of the week.  Please try again...")

    #prints line break and saves user input for later
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
    # loads city data file into dataframe named df
    if city != 'all':
        df = pd.read_csv(CITY_DATA[city])
    # 'all' combines every city's file into one dataframe named df
    else:
        df = pd.concat(map(pd.read_csv, [CITY_DATA[city] for city in CITY_DATA]), ignore_index=True)

    # converts Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['month'] = df['month'].str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['day_of_week'] = df['day_of_week'].str.lower()
    df['hour'] = df['Start Time'].dt.hour
    
    
    # filter by month if applicable
    if month != 'all':
       # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month: ",df['month'].mode()[0])
    
    # display the most common day of week
    print("Most common day: ",df['day_of_week'].mode()[0])

    # display the most common start hour
    print("Most common start hour: ",df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used Start Station: ",df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most commonly used End Station: ",df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("Most frequent combonation of stations for a trip is between:",(df['Start Station'] + ' and ' + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: " + str(round(df['Trip Duration'].sum())) + " seconds")
    
    # display mean travel time
    print("Average total travel time: " + str(round(df['Trip Duration'].mean())) + " seconds")
    
    # display longest travel time
    print("Longest single travel time: " + str(round(df['Trip Duration'].max())) + " seconds")
    
    # display shortest travel time
    print("Shortest single travel time: " + str(round(df['Trip Duration'].min())) + " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User types and count:\n" + str(df['User Type'].value_counts()) + "\n")

    # Display counts of gender
    if 'Gender' in df.columns and 'Birth Year' in df.columns:
        print("Gender and count:\n" + str(df['Gender'].value_counts()) + "\n")
        
        # Display earliest, most recent, and most common year of birth
        print("Earliest birth year: ", int(df['Birth Year'].min()))
        print("Most recent birth year: ", int(df['Birth Year'].max()))
        print("Most common birth year: ", int(df['Birth Year'].mode()))
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def show_raw_data(df):
    """Asks user if they want to view the raw data, five rows at a time."""
    raw_data = str(input("\nAre you interested in seeing the raw data? Enter yes or no: ").lower())
    raw = 0
    while raw_data == 'yes':
            for i in range(raw,raw+5,5):
                print("\n" + str(df.iloc[raw:raw+5]))
                raw += 5
                raw_data = str(input("\nWant to see more data? Enter yes or no: ").lower())
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("\nThanks for sharing the rideshare data with me!  Have a great day!")
            break


if __name__ == "__main__":
	main()
