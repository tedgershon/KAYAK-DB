import psycopg2
from pprint import pprint as pp
from prettytable import PrettyTable

import re

# helpful functions to print data / table
SHOW_CMD = True

def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)

# The following method works if you pre-specify columns as a parameter 'cols = []'
def show_table(rows, cols='', ncols=None):
    if ncols != None:
        cols = [('c%d' % i) for i in range(1, ncols+1)]
    # else:
        # cols = cols.split()
    table = PrettyTable( cols )
    table.add_rows(rows)
    print(table)

def print_table(table, cols=''):
    print_me = f'''
        SELECT * FROM {table}
    '''
    cur.execute(print_me)
    rows = cur.fetchall()
    show_table(rows, cols)

# connect to project db
conn = psycopg2.connect(database='project', user='isdb') 
conn.autocommit = True
cur = conn.cursor()

# User story definition
us='''
* Simple Analytical US: Find Quickest Trip

   As a:  Traveler
 I want:  To find the quickest trip
So That:  I can spend the least amount of time on an airplane
'''
print(us)

# US4 -- Find quickest trip
def quickest_trip(a_from, a_to, date): # params of flight (i.e. to/from airport, date)
    
    tmpl = ''' 
        WITH quickest_trip AS (SELECT MIN(arrival_time - departure_time) AS Duration
                                 FROM Flight
                                WHERE departure_airport = %s AND destination_airport = %s
                                                             AND departure_date = CAST(%s AS DATE))

        SELECT (arrival_time - departure_time) AS Duration, flight_id, departure_time, arrival_time, seats_available, airline_id
          FROM Flight
         WHERE departure_airport = %s AND destination_airport = %s
                                      AND departure_date = CAST(%s AS DATE)
                                      AND (arrival_time - departure_time) = (SELECT duration FROM quickest_trip)
    '''
    cmd = cur.mogrify(tmpl, (a_from, a_to, date, a_from, a_to, date))
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    if rows:
          columns = ['Duration', 'flight_id', 'departure_time', 'arrival_time', 'seats_available', 'airline_id']
          show_table(rows, cols=columns)
    else:
        print(f"No flights found from {a_from} to {a_to} on {date}.") # insert parameters

# helper function to demonstrate US4
def print_quickest(from_loc, to_loc, day):
    print(f"\nExecuting user story from", from_loc, "to", to_loc, "on", day)
    print(f"Finds flight durations on Flight table, filters rows from", from_loc, "to", to_loc, "on", day)
    print(f"Quickest flight from {from_loc} to {to_loc} on {day}:")
    quickest_trip(from_loc, to_loc, day)

# description of user story
print("US4: finds the quickest trip given departure and destination airports and a date\n")

#print tables before querying
print("Flight table before querying:")
print("Flight Table:")
print_table("Flight", ['flight_id', 'departure_date', 'departure_airport', 'destination_airport', 'departure_time', 'arrival_time', 'seats_available', 'airline_id'])

#execute user stories
print_quickest("PIT","NYC","11/19/2024")
print_quickest("PIT","LAX","11/24/2024")
print_quickest("PIT","DEN","11/24/2024")

# Run python script with the following command:
    # % python us4-find-quickest_trip-simple-analytical.py