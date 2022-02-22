import time
import pandas as pd
import numpy as np
from datetime import date

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US Bikeshare data!\n')

    ##### -- USER INPUT: CITY -- #####
    # get user input for city (Chicago, New York City, Washington)
    print("Which city would you like to get information on?")
    print("- Chicago\n- New York City\n- Washington")
    
    city = input().title()
    if city == 'New York':
        city = 'New York City'

    #Validate user input
    while city!='Chicago' and city!='New York City' and city!='Washington':
        print('\nInvalid input!\nPlease pick one of these cities:')
        print("- Chicago\n- New York City\n- Washington")
        city = input().title()

        if city == 'New York':
            city = 'New York City'
    print('\n')

    #Ask user if they want to filter data by month, day or both
    filter = input('Would you like to filter the data by:\n- Month\n- Day\n- Both\n- None\n').title()

    while filter!='Month' and filter!='Day' and filter!='Both' and filter!='None':
        print('\nInvalid input!\nPlease pick if you\'d like to filter the data by:')
        filter = input('- Month\n- Day\n- Both\n- None\n').title()

    print('\n')
    if filter=='Month' or filter=='Both':
    ##### -- USER INPUT: MONTH -- #####
        # get user input for month (all, january, february, ... , june)
        print("Which month would you like to get information on?")
        print("- January\n- February\n- March\n- April\n- May\n- June")

        month = input().title()

        #Validate user input
        while month!='January' and month!='February' and month!='March' and  month!='April' and  month!='May' and  month!='June':
            print('\nInvalid input!\nPlease pick a month:')
            print("- January\n- February\n- March\n- April\n- May\n- June")

            month = input().title()
        print('\n')
    else:
        month = 'all'

    if filter=='Day' or filter=='Both':
    ##### -- USER INPUT: DAY OF WEEK -- #####
        # get user input for day of week (all, monday, tuesday, ... sunday)
        print("Which day of the week would you like to get information on?")
        print("- Sunday\n- Monday\n- Tuesday\n- Wednesday\n- Thursday\n- Friday\n- Saturday")
        
        day = input().title()

        #Validate user input
        while day!='Sunday' and day!='Monday' and day!='Tuesday' and  day!='Wednesday' and  day!='Thursday' and  day!='Friday' and  day!='Saturday':
            print('\nInvalid input!\nPlease pick a day:')
            print("- Sunday\n- Monday\n- Tuesday\n- Wednesday\n- Thursday\n- Friday\n- Saturday")

            day = input().title()
        print('\n')
    else:
        day = 'all'
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
        df - pandas DataFrame containing city data filtered by city, month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = pd.to_datetime(df['Start Time']).dt.month
    df['Day_of_week'] = pd.to_datetime(df['Start Time']).dt.day_name()
    #df['Day_of_week'] = pd.to_datetime(df['Start Time']).dt.weekday_name   #for older pd version (Pandas 0.18.1+)

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6}
    
        # filter by month to create the new dataframe
        df = df[df['Month']==month_dict[month]]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_week']==day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most and least frequent times of travel."""

    print('\nCalculating The Most and Least Frequent Times of Travel...\n')
    start_time = time.time()

    # --- MONTH STATS ---
    if month=='all':
        print('-- MONTH STATS --')
        month_dict = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}

        # display the most common month
        popular_month = month_dict[df.mode()['Month'][0]]
        print("Most popular month: ",popular_month)
        # display the least common month
        least_popular_month = month_dict[df['Month'].value_counts().idxmin()]
        print("Least popular month: ",least_popular_month)
        print()

    # --- DAY STATS ---
    if day=='all':
        print('-- DAY STATS --')
        # display the most common day of week
        popular_day = df.mode()['Day_of_week'][0]
        print("Most popular day: ",popular_day)
        # display the least common day of week
        least_popular_day = df['Day_of_week'].value_counts().idxmin()
        print("Least popular day: ",least_popular_day)
        print()

    # --- HOUR STATS ---
    print('-- HOUR STATS --')
    #START HOUR
    # extract hour from the Start Time column to create a Start Hour column
    df['Start Hour'] = pd.to_datetime(df['Start Time']).dt.hour
    # display the most common start hour
    popular_hour = int(df.mode()['Start Hour'][0])
    print('Most popular start hour:', popular_hour)
    # display the least common start hour
    least_popular_hour = df['Start Hour'].value_counts().idxmin()
    print("Least popular start hour: ",least_popular_hour)

    #END HOUR
    # extract hour from the End Time column to create a End Hour column
    df['End Hour'] = pd.to_datetime(df['End Time']).dt.hour
    # display the most common start hour
    popular_endhour = int(df.mode()['End Hour'][0])
    print('Most popular end hour:', popular_endhour)
    # display the least common start hour
    least_popular_endhour = df['End Hour'].value_counts().idxmin()
    print("Least popular end hour: ",least_popular_endhour)
    
    print()

    print("\nThis took %s seconds to compute." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most and Least Popular Stations and Trip...\n')
    start_time = time.time()

    print('-- STATION STATS --')
    # display most commonly used start station
    popular_start_station = df.mode()['Start Station'][0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df.mode()['End Station'][0]
    print('Most popular end station:', popular_end_station)
    print()
    # display least commonly used start stations
    # get the value counts of `Start Station`
    vc_start = df['Start Station'].value_counts()
    # get the min number
    vc_min_start = vc_start.min()
    # boolean for which station has the min number
    vc_is_min_start = vc_start.eq(vc_min_start)
    # list of start station(s) with the min count value
    vc_min_start_list = list(vc_is_min_start[vc_is_min_start].index)
    # loop and display
    # if number of stations exceed 5, show the user only 5 of them
    if len(vc_min_start_list)>5:
        print('5 of the least popular start station(s): -',vc_min_start_list[0])
        for i in range(4):
            print('                                         -',vc_min_start_list[i+1])

    else:
        print('Least popular start station(s): -',vc_min_start_list[0])
        for i in range(len(vc_min_start_list)-1):
            print('                                -',vc_min_start_list[i+1])


    # display least commonly used end stations
    # get the value counts of `End Station`
    vc_end = df['End Station'].value_counts()
    # get the min number
    vc_min_end = vc_end.min()
    # boolean for which station has the min number
    vc_is_min_end = vc_end.eq(vc_min_end)
    # list of start station(s) with the min count value
    vc_min_end_list = list(vc_is_min_end[vc_is_min_end].index)
    # loop and display
    # if number of stations exceed 5, show the user only 5 of them
    if len(vc_min_end_list)>5:
        print('5 of the least popular end station(s): -',vc_min_end_list[0])
        for i in range(4):
            print('                                       -',vc_min_end_list[i+1])

    else:
        print('Least popular end station(s): -',vc_min_end_list[0])
        for i in range(len(vc_min_end_list)-1):
            print('                              -',vc_min_end_list[i+1])


    # display most frequent combination of start station and end station trip
    print('\nMost frequent combination of start station and end station trip:')
    # get the value counts of `Start Station` and `End Station`
    start_to_end = df[['Start Station','End Station']].value_counts()
    # get max number 
    maxnum_start_to_end = start_to_end.max()
    # boolean for which start & end stations have the max num
    is_max_start_to_end = start_to_end.eq(maxnum_start_to_end)
    # list of start and end station with the most frequent combination
    max_start_to_end = list(is_max_start_to_end[is_max_start_to_end].index)
    
    if len(max_start_to_end)==1:
        print('- Start station: ', max_start_to_end[0][0])
        print('- End station: ', max_start_to_end[0][1])
    else:
        i = len(max_start_to_end)
        print('There are {} combinations.'.format(i))
        # if combinations are more than 3, display only 3
        if i>3:
            print('3 of them are: ')
            x = 0
            for stations in max_start_to_end:
                print('- Start station: ', stations[0])
                print('- End station: ', stations[1])
                print()
                x+=1
                if x==3:
                    break
        # display all combinations if they are less than or equal 3, and more than 1
        else:
            for stations in max_start_to_end:
                print('- Start station: ', stations[0])
                print('- End station: ', stations[1])
                print()

    print("\nThis took %s seconds to compute." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('-- TRAVEL STATS --')
    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is: {} minutes -> approx {} hours.'.format(total_time, total_time//60))

    # display average travel time
    mean_time = df['Trip Duration'].mean()
    print('The average travel time is: {} minutes -> approx {} hours.'.format("{:.2f}".format(mean_time), "{:.2f}".format(mean_time//60)))

    # display standard deviation of travel time
    std_time = df['Trip Duration'].std()
    print('The standard deviation of travel time is: {} minutes -> approx {} hours.'.format("{:.2f}".format(std_time), "{:.2f}".format(std_time//60)))

    # display maximum travel time
    max_time = df['Trip Duration'].max()
    print('The maximum travel time is: {} minutes -> approx {} hours.'.format(int(max_time), int(max_time//60)))

    # display minimum travel time
    min_time = df['Trip Duration'].min()
    print('The minimum travel time is: {} minutes -> approx {} hours.'.format(int(min_time), int(min_time//60)))

    print("\n\nThis took %s seconds to compute." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('-- USER STATS --')

    # Display counts of user types
    # bool if the user if a subsriber
    is_subs = df['User Type']=='Subscriber'
    # count num of Subscribers
    subs_count = is_subs[is_subs].count()
    # bool if the user if a customer
    is_cus = df['User Type']=='Customer'
    # count num of Customers
    cus_count = is_cus[is_cus].count()
    print('Number of subscribers: ', subs_count)
    print('Number of customers: ', cus_count)

    if city=='Chicago'or city=='New York City':
        # Display counts of gender
        is_male = df['Gender']=='Male'
        male_count = is_male[is_male].count()
        is_female = df['Gender']=='Female'
        female_count = is_female[is_female].count()

        print('\nTotal number of males: ',male_count)
        print('Total number of females: ',female_count)

        # Display earliest, most recent, and most common year of birth
        # edit df to contain only reasonable years (1900 to current year)
        df2 = df[df['Birth Year'].between(1900, date.today().year)]

        # earliest year of birth
        oldest = int(df2['Birth Year'].min())
        
        # latest year of birth
        youngest = int(df2['Birth Year'].max())
        
        print('\nEarliest year of birth: ', oldest)
        print('This user is {} years old'.format(date.today().year-oldest))
        print('\nLatest year of birth: ', youngest)
        print('This user is {} years old'.format(date.today().year-youngest))
        print('\nMost common year of birth: ', int(df['Birth Year'].mode().values[0]))

    print("\n\nThis took %s seconds to compute." % (time.time() - start_time))
    print('-'*40)


def sample_data(df):
    """Displays saw raw data."""

    # ask the user if they want to view the sample raw data
    rawdata = input('\nWould you like to see a sample of the raw data? Enter yes or no.\n').lower()
    #validation
    while rawdata != 'yes' and rawdata != 'no':
        print('\nInvalid input!')
        rawdata = input('Would you like to see a sample of the raw data? Enter yes or no.\n').lower()
    if rawdata == 'no':
        print('-'*40)
        return None
    else:
        # print 3 samples of raw data each time the users enters 'yes'
        print('\n-- USER STATS --')
        df.pop('Unnamed: 0')
        i=0
        while rawdata == 'yes':
            print(df.iloc[i],'\n')
            print(df.iloc[i+1],'\n')
            print(df.iloc[i+2],'\n')
            i += 1
            rawdata = input('Would you like to see 3 more samples? Enter yes or no.\n').lower()
            while rawdata != 'yes' and rawdata != 'no':
                print('\nInvalid input!')
                rawdata = input('Would you like to see 3 more samples? Enter yes or no.\n').lower()
            print()
    
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()

        if month!='all' and day!='all':
            print('\nAnalyzing Bikeshare Data in {}, in {}, on {}...'.format(city, month, day))
        elif month!='all':
            print('\nAnalyzing Bikeshare Data in {}, in {}...'.format(city, month))
        elif day!='all':
            print('\nAnalyzing Bikeshare Data in {}, on {}...'.format(city, day))
        else:
            print('\nAnalyzing Bikeshare Data in {}...'.format(city))
        
        df = load_data(city, month, day)
        print()
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        sample_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart != 'yes' and restart != 'no':
            print('\nInvalid input!')
            restart = input('Would you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break
        print('-'*40)


if __name__ == "__main__":
	main()
