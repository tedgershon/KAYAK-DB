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
* Complex Operational US: Filter Airlines

   As a:  Traveler
 I want:  To only see flights for a specific airline
So That:  I can book with my preferred airline and use loyalty points
'''
print(us)

# US1 -- Filter airlines
def filter_airlines(airline):
    
    tmpl = ''' 
        SELECT f.flight_id, f.departure_date, f.departure_airport, f.destination_airport, f.departure_time, f.arrival_time, f.seats_available          
          FROM Flight AS f
          JOIN Airline AS a
            ON f.airline_id = a.airline_id
         WHERE a.name ILIKE %s
    '''
    cmd = cur.mogrify(tmpl, (f"%{airline}%",)) # allows %s to work even if partial airline name typed
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    if rows:
          columns = ['flight_id', 'departure_date', 'departure_airport', 'destination_airport', 'departure_time', 'arrival_time', 'seats_available']
          show_table(rows, cols=columns)
    else:
        print(f"No flights found for airline {airline}.")

# helper function to demonstrate US1
def airline_flights(airline_name):
    print(f"\nExecuting user story for", airline_name)
    print(f"Joins Flight and Airline tables, filters rows where airline name is", airline_name)
    print(f"Flights for {airline_name}:")
    filter_airlines(airline_name)

# description of user story
print("US1: provides flights for a specified airline\n")

#print tables before querying
print("Flight and Airline tables before querying:")
print("Flight Table:")
print_table("Flight", ['flight_id', 'departure_date', 'departure_airport', 'destination_airport', 'departure_time', 'arrival_time', 'seats_available', 'airline_id'])
print("Airline Table:")
print_table("Airline", ['airline_id', 'name'])

#execute user stories
airline_flights("American Airlines") #this also works for partial word --> i.e. just "american"
airline_flights("United Airlines")
airline_flights("Spirit Airlines")
airline_flights("Delta Airlines")
airline_flights("Alaska Airlines")

# Run python script with the following command:
    # % python us1-filter-airlines-complex-operational.py