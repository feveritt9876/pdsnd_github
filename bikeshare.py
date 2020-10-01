import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('Which city would you like to see data for? \nPlease choose from Chicago, New York City or Washington:  ').lower()
        if city not in cities:
            print('Sorry, this is not one of the cities avaliable in the dataset. Please try again!')
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input('Which month would you like to see data for? \nJanuary, February, March, April, May, June, or all?:  ').lower()
        if month not in months:
            print('Sorry, this month is not in our database. Please try again!')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('What day of the week would you like to see data for? \nMonday, Tuesday, Wednesday, Thursday, Friday or all?:  ').lower()
        if day not in days:
            print('Sorry, this is an invalid weekday. Please try again!')
        else:
            break

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
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #extract month and day of the week from Start time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday


    #filter by month if applicable
    if month != 'all':
        months= ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+ 1
    #filter by month to create the new dataframe
        df = df[df['month'] ==month]

    #filter by day of week if applicable
    if day != 'all':
        day_name= ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day= day_name.index(day)+1
    #filter by day of the week to create the new datarame
        df=df[df['day_of_week'] ==day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month= df['month'].mode()[0]
    print('Most common month:', common_month)

    # display the most common day of week
    common_day= df['day_of_week'].mode()[0]
    print('Most common day of week:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour of the day:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # display most commonly used end station
    # display most frequent combination of start station and end station trip
    popular_start = df['Start Station'].mode()[0]

    popular_end= df['End Station'].mode()[0]

    popular_trip= df.groupby(['Start Station', 'End Station']).size().nlargest(1)

    print("\nThe most popular start station is: {} \
  \nThe most popular end station is: {} \
  \nThe most popular trip from start to end is:\n{}".format(popular_start, popular_end, popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time= df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    count_of_user_types = df['User Type'].value_counts()
    print('The number of users:\n', count_of_user_types)

    # Display counts of gender: note missing data in washington dataset
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('gender count:', gender)
    else:
        print('Gender does not exist in data')

    # Display earliest, most recent, and most common year of birth: note missing data in washington dataset
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']

        print('Earliest birth year:', birth_year.min())

        print('Most recent birth year:', birth_year.max())

        print('Most common birth year:', birth_year.mode()[0])
    else:
        print('Birth dates do not exist in data')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def rows(df):
    """ Displays the first 5 rows of the raw data. Note to self row numbers will change depending on inputs."""

    display_more=input('Do you want to see 5 rows of the raw data? Enter yes or no.\n').lower()
    if display_more == ('yes'):
        i = 0
        while True:
            print(df.iloc[i: i+5])
            i += 5
            even_more = input('Would you like to see 5 more rows? Enter yes or no\n').lower()
            if even_more not in ('yes'):
                break

        print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rows(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    # Below line will indicate python runtime to find a function named main() in the program file as first thing

if __name__ == "__main__":
	main()
