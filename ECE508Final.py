#############################################################################################
# Author: Ming Ma, Zhe Lu                                                                   #
# Project Name: TriMet Red Line Train Schedule Check Tool(GUI)                              #
# Final Project of ECE 508: Python Workshop                                                 #
#############################################################################################
# Description: User can choose the Direction of the red line train and their boarding       #
# location. After choose these two places, click Get Table Button first, then click         #
# Set Location Button. After this, user can enter the time that they want to ride the train #
# in format of HH:MMam/pm. For example, one person wants to ride the train at 9:30am or at  #
# 10:35pm. Only one time is permitted to enter. After entering the time, click Updata Button#
# and the software will get the information from TriMet Websites to get information and     #
# calculate three nearset waiting time. If there aren't trains available, No Train Available#
# will show in the Wait Time Entry. The Clear Button can be used to clear Travel Time and   #
# Wait Time boxes to re-enter new Travel Time. Some of the trains will become blue lines    #
# after some stations at midnight. This situation is not considered in this program.        #
#############################################################################################
# How to operation: Select Direction -> Click Get Table -> Select Location -> Click Set     #
# Locaton Take a look at the input formate -> Click Clear Button -> Enter Tranvel Time      #
# -> Click Update                                                                           #
#############################################################################################
import requests
from bs4 import BeautifulSoup  # Use BeautifulSoup to get the information from Trimet Website
import tkinter as tk  # Use tiinter to organize the GUI
from tkinter import ttk
from datetime import datetime  # Use datatime to do some operations based on time


# This function will generate a dictionary which contains the information of the time schedules
# of different stations. Keys are the station information and values are the relevant shcedule.
# Input: station_info: tuple or list which contains the information of different stations.
#       time_info: List contains the time schedule. Elements in list are also list which
# contains the time schedule of different stations.
def get_train_info(station_info, time_info):
    train_info = {}
    time_list = []
    for index in range(1, len(time_info)):
        for index2 in range(0, len(time_info[index].find_all('td'))):
            if time_info[index].find_all('td')[index2].text[0].isdigit() == True:
                if time_info[index].find_all('td')[index2].text[-1] == 'X':
                    time_list.append(time_info[index].find_all('td')[index2].text[:-1])
                else:
                    time_list.append(time_info[index].find_all('td')[index2].text)
        train_info[station_info[index - 1].find('h6').text] = time_list
        time_list = []
    return train_info


# This function will convert the time format from 12am/pm to 24 hours. So, we can
# do some operations.
def convert24(Intime):
    # Checking if last two elements of time
    # is am and first two elements are 12
    if Intime[-2:] == "am" and Intime[:2] == "12":
        return "00" + Intime[2:-2]

        # remove the am
    elif Intime[-2:] == "am":
        return Intime[:-2]

        # Checking if last two elements of time
    # is pm and first two elements are 12
    elif Intime[-2:] == "pm" and Intime[:2] == "12":
        return Intime[:-2]

    # add 12 to hours and remove PM
    elif Intime[1] == ":":
        return str(int(Intime[:1]) + 12) + Intime[1:4]
    elif Intime[2] == ":":
        return str(int(Intime[:2]) + 12) + Intime[2:5]


# This function is executed when user presses Get Table Button.
# Based on the user's choice, this function will generate a dictionary which
# contains the station information and its relevant time schedule.
def get_table():
    station_dictionary = {}
    # Link to different website based on the user's choices.
    if selected_direction.get() == 'TriMet: MAX Red Line Weekday To Portland City Center and Airport':
        r = requests.get('https://trimet.org/schedules/w/t1090_0.htm')
    elif selected_direction.get() == 'TriMet: MAX Red Line Weekday To Portland City Center and Beaverton Transit Center':
        r = requests.get('https://trimet.org/schedules/w/t1090_1.htm')
    elif selected_direction.get() == 'TriMet: MAX Red Line Saturday To Portland City Center and Airport':
        r = requests.get('https://trimet.org/schedules/s/t1090_0.htm')
    elif selected_direction.get() == 'TriMet: MAX Red Line Saturday To Portland City Center and Beaverton Transit Center':
        r = requests.get('https://trimet.org/schedules/s/t1090_1.htm')
    elif selected_direction.get() == 'TriMet: MAX Red Line Sunday To Portland City Center and Airport':
        r = requests.get('https://trimet.org/schedules/h/t1090_0.htm')
    elif selected_direction.get() == 'TriMet: MAX Red Line Sunday To Portland City Center and Beaverton Transit Center':
        r = requests.get('https://trimet.org/schedules/h/t1090_1.htm')
    soup = BeautifulSoup(r.text, 'html.parser')  # use BeautifulSoup to parse information from website.
    time_results = soup.find_all('table')  # Find all information after <table and end with </table>
    station_results = soup.find_all('th')  # Find all information after <th> and end with </th>
    # Combine stations with relevant schedules and put them into a dictionary.
    station_dictionary = get_train_info(station_results, time_results)
    return station_dictionary


# This function is executed when user presses the Set Location Button.
# This will return a list which contains the time schedule of the selected station.
def set_curt_location():
    station_dictionary = get_table()
    return station_dictionary[selected_location.get()]


# This function is executed when user presses the Update Button.
# It will get the input time from user and calculate the nearest 3 wait time.
def update_info():
    time_list = []
    wait_list = []  # list which conatins the wait time.
    time_list = set_curt_location()
    departure_time = input_time_hrs.get() + ':' + input_time_mins.get() + selected_time.get()  # Get the input time from the user.
    print(departure_time)
    if departure_time[-2:] == "am" or departure_time[-2:] == "pm":
        departure_time_24 = convert24(departure_time)
        print(time_list)  # print the time schedule of the selected station in case of the GUI doesn't work.
        for time in time_list:
            train_time = convert24(time)
            time_diff = calculate_time_diff(departure_time_24, train_time)
            if time_diff > compare_time0:  # Check if the time differences are reasonable.
                try:
                    wait_list.append(time_diff)
                except:
                    print("No Train is available")
        wait_list.sort()  # sort the wait_list in order to get the most smallest 3 wait time.
        # Get at most smallest 3 wait time.
        if len(wait_list) >= 3:
            print_wait = str(wait_list[0])[:-3] + " " + str(wait_list[1])[:-3] + " " + str(wait_list[2])[:-3]
        elif len(wait_list) == 2:
            print_wait = str(wait_list[0])[:-3] + " " + str(wait_list[1])[:-3]
        elif len(wait_list) == 1:
            print_wait = str(wait_list[0])[:-3]
        else:
            print_wait = "No Train Available"
        wait_time.set(print_wait)
    else:
        input_time_hrs.set("Input Format is Wrong")


# Calculate the time difference between the available train time and user input time.
def calculate_time_diff(departure_time, train_time):
    FMT = '%H:%M'  # Define the output format.
    # Need to convert into time instance to do some calculations based on time.
    tdelta = datetime.strptime(train_time, FMT) - datetime.strptime(departure_time, FMT)
    return tdelta


# This function will execute when user presses Clear Button. So, user can enter
# travel time multiple times.
def clear_windows():
    # selected_direction.set("")
    # selected_location.set("")
    input_time_hrs.set("")
    input_time_mins.set("")
    wait_time.set("")


# Get the time instance which stand for 00:00 in HH:MM. This will be used to
# examine the wait times are reasonable or not.
d = convert24("0:00am")
compare_time0 = calculate_time_diff(d, d)

# The following part will generate our GUI.
parent = tk.Tk()
parent.title('Red Line MAX Schedule')

tk.Label(parent,
         text="Select Direction -> Click Get Table -> Select Location -> Click Set Location -> Click Clear -> Enter Travel time -> Click Update").grid(
    row=0, columnspan=3)
tk.Label(parent, text="Direction:").grid(row=1, column=0, sticky='w', pady=2)
# Tuple which contains the information of directions of Red line trains.
choices_direction = ('TriMet: MAX Red Line Weekday To Portland City Center and Airport',
                     'TriMet: MAX Red Line Weekday To Portland City Center and Beaverton Transit Center',
                     'TriMet: MAX Red Line Saturday To Portland City Center and Airport',
                     'TriMet: MAX Red Line Saturday To Portland City Center and Beaverton Transit Center',
                     'TriMet: MAX Red Line Sunday To Portland City Center and Airport',
                     'TriMet: MAX Red Line Sunday To Portland City Center and Beaverton Transit Center')
selected_direction = tk.StringVar()
w = ttk.Combobox(parent, values=choices_direction, textvariable=selected_direction, width=72).grid(row=1, column=1,
                                                                                                   sticky='w', pady=2)

tk.Button(parent, text="Get Table", command=get_table, width=10).grid(row=1, column=2, sticky='w')

tk.Label(parent, text="Location:").grid(row=2, column=0, sticky='w', pady=2)
# Tuple which contains the information of stations.
choices_location = ('Beaverton TC MAX Station', 'Sunset TC MAX Station',
                    'Washington Park MAX Station', 'Providence Park MAX Station',
                    'Pioneer Square South MAX Station', 'Rose Quarter TC MAX Station',
                    'Hollywood/NE 42nd Ave TC MAX Station', 'Gateway/NE 99th Ave TC MAX Station',
                    "Portland Int'l Airport MAX Station")

selected_location = tk.StringVar()
w = ttk.Combobox(parent, values=choices_location, textvariable=selected_location, width=72).grid(row=2, column=1,
                                                                                                 sticky='w', pady=2)
tk.Button(parent, text="Set Location", command=set_curt_location).grid(row=2, column=2, sticky='w')

tk.Label(parent, text="Travel Time(HH):").grid(row=3, column=0, sticky='w' + 'n', pady=2)
input_time_hrs = tk.StringVar()
tk.Entry(parent, width=15, textvariable=input_time_hrs).grid(row=3, column=1, sticky='w', pady=2)
input_time_hrs.set("Input Format: HH")  # Prompting Information
input_time_mins = tk.StringVar()
tk.Label(parent, text="Travel Time(MM):").grid(row=4, column=0, sticky='w' + 'n', pady=2)
tk.Entry(parent, width=15, textvariable=input_time_mins).grid(row=4, column=1, sticky='w', pady=2)
input_time_mins.set("Input Format: MM")  # Prompting Information
tk.Label(parent, text="Travel Time(am/pm):").grid(row=5, column=0, sticky='w', pady=2)
# Tuple which contains the information of stations.
choices_time = ('am', 'pm')
selected_time = tk.StringVar()
select_time = ttk.Combobox(parent, values=choices_time, textvariable=selected_time, width=15).grid(row=5, column=1,
                                                                                                sticky='w', pady=2)




tk.Label(parent, text="Wait Time:").grid(row=6, column=0, sticky='w' + 'n')
wait_time = tk.StringVar()
tk.Entry(parent, width=30, textvariable=wait_time).grid(row=6, column=1, sticky='w')
wait_time.set("Output Format: HH:MM")  # Prompting Information

tk.Button(parent, text="Clear", width=10, command=clear_windows).grid(row=3, column=2, sticky='w')
tk.Button(parent, text="Update", command=update_info, width=10).grid(row=4, column=2, sticky='w')

parent.mainloop()


