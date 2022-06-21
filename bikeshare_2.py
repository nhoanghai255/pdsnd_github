import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    city = input('Enter City :').lower()
    while city not in CITY_DATA:
        print('Please enter the correct city! Hint: The city should be chicago or new york city or washington')
        city = input('Enter City:').lower()

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march', 'apr', 'may', 'june']
    month = input('Enter Month: ').lower()
    while month not in valid_months:
        print('Please enter the correct month! Hint: The month should be from Jan to Jun or All')
        month = input('Enter Month:').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Enter Day of Week: ').lower()
    while day not in valid_days:
        print('Please enter the correct day of week!')
        day = input('Enter Day of Week:').lower()

    print('-' * 40)
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
    # Load data from CSV file by name
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))

    # Convert the Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter data by month
    if month != 'all':
        months = ['january', 'february', 'march', 'apr', 'may', 'june']
        month = months.index(month) + 1
        df[df['month'] == month]

    # Filter data by day
    if day != 'all':
        df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['january', 'february', 'march', 'apr', 'may', 'june']

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is: ", months[most_common_month - 1].title())

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of week is: ", most_common_day_of_week)

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['start_hour'].mode()[0]
    print("The most common start hour is: ", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is: ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is: ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combination_stations = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination is: ", most_frequent_combination_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    print("Total travel time is: ", df['Travel Time'].sum())

    # display mean travel time
    print("Average travel time is: ", df['Travel Time'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print("User Types in counting: ", df['User Type'].value_counts())

    try:
        # Display counts of gender
        print("User Types in counting: ", df['Gender'].value_counts())
    except:
        print("Data is not available!")

    try:
        # Display earliest, most recent, and most common year of birth
        print("The earliest year of birth is: ", df['Birth Year'].min())

        print("The most recent year of birth is: ", df['Birth Year'].max())

        print("The most common year of birth is: ", df['Birth Year'].mode()[0])
    except:
        print("Data is not available!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Allow user to view the raw data
        view_data = input('\nWould you like to view the raw data? Enter yes or no.\n')
        count = 0
        while view_data.lower() == 'yes':
            if count >= df.shape[0]:
                print("All of records was displayed")
                break
            else:
                print(df.iloc[count:count + 5])
                count = count + 5
                view_data = input('\nWould you like to view the next 5 records? Enter yes or no.\n')
        if view_data.lower() != 'yes':
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
