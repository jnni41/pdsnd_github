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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to explore? Please enter Chicago, New York City, or Washington: ")
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print("City unrecognized, please try again.")
        else:
            break

    while True:
        data_filter = input('Would you like to filter by month, day of the week, both, or none? ')

        if data_filter.lower() not in ('month', 'day', 'day of week', 'day of the week', 'both', 'none'):
            print("Filter unrecognized, please try again.")
        elif data_filter.lower() == 'month':
            day = 'all'
            while True:
                month = input("Please enter Jan, Feb, Mar, Apr, May, Jun: ")
                if month.lower() not in ('jan', 'feb', 'mar', 'apr', 'may', 'jun'):
                    continue
                else:
                    break
            break
        elif data_filter.lower() in ('day', 'day of week', 'day of the week'):
            month = 'all'
            while True:
                day = input("Please enter a day of the week (Monday, Tuesday, etc.): ")
                if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                    continue
                else:
                    break
            break
        elif data_filter.lower() == 'both':
            while True:
                month = input("Please enter Jan, Feb, Mar, Apr, May, Jun: ")
                if month.lower() not in ('jan', 'feb', 'mar', 'apr', 'may', 'jun'):
                    continue
                else:
                    break
            while True:
                day = input("Please enter a day of the week (Monday, Tuesday, etc.): ")
                if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                    continue
                else:
                    break
            break
        else:
            day = 'all'
            month = 'all'
            print('We will examine all data from', city.title())
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_name = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    popular_month = df['month'].mode()[0]
    popular_month_name = month_name[popular_month]

    print('Most Common Month Is:', popular_month_name)

    # TO DO: display the most common day of week
    popular_day = df['day'].mode()[0]

    print('Most Common Day Is: ', popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most Popular Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most Popular End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_combo_start_stop_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)

    print('Most Popular Combination of Start/Stop Stations:\n', popular_combo_start_stop_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # TO DO: display mean travel time
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    def ddhhmmss(trip_stat,trip_time):
        """
        Converts seconds to days, hours, minutes and seconds using divmod

        Input:
        (str) trip_stats - describes what sort of travel time (max, min, average, etc) for descriptive output
        (float) trip_time - calculated number of seconds

        Output:
        Prints statement with calculations of DDHHMMSS in sentence form
        """
        days = divmod(trip_time, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)

        print(trip_stat, "Travel Time: {} days, {} hours, {} minutes, {} seconds (or {} seconds)".format(days[0], hours[0], minutes[0], minutes[1], trip_time))

    ddhhmmss("Total",total_travel_time)
    ddhhmmss("Mean",mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
    else:
        gender_types = "No gender data to display."

    print(gender_types)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birthyear = int(df['Birth Year'].min())
        most_recent_birthyear = int(df['Birth Year'].max())
        most_common_birthyear = int(df['Birth Year'].mode()[0])
        print("Earliest Birth Year:", earliest_birthyear)
        print("Most Recent Birth Year:", most_recent_birthyear)
        print("Most Common Birth Year:", most_common_birthyear)
    else:
        print("No birth year data to display.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city.lower(), month.lower(), day.lower())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Asks user for next steps: restart program, see raw data, or exit the program
        restart_or_data = input('\nWhat would you like to do next?\nPlease enter restart, see data, or exit\n')
        if restart_or_data.lower() == 'restart':
            continue
        elif restart_or_data.lower() in ('see data', 'data'):
            i = 0
            pd.set_option('display.max_columns',10)
            while True:
                print(df.iloc[i:i+5])
                i += 5
                more_data = input('Would you like to see more data? Please enter yes or no: ')
                if more_data.lower() != 'yes':
                    break
            restart = input('Would you like to restart? Please enter yes or no: ')
            if restart.lower() != 'yes':
                break
        else:
            break


if __name__ == "__main__":
	main()
