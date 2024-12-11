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
* Simple Operational US: Provide Seating Availability

   As a:  Airline
 I want:  To tell users of Kayak how many seats are left in a specified flight for all flights
So That:  I can help users make more informed decisions about what and when to book
'''
print(us)

# US10 -- Provide seating availability
def available_seats(flight_id, departure_date):
    
    tmpl = ''' 
        SELECT flight_id, departure_date, seats_available
          FROM Flight
         WHERE flight_id = %s and departure_date = %s
    '''
    cmd = cur.mogrify(tmpl, (flight_id, departure_date))
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    columns = ["Flight ID", "Departure Date", "Seats Available"]
    show_table(rows, cols=columns)

# helper function to demonstrate US10
def show_available_seats(flight_id, departure_date):
    print(f"\nExecuting user story for flight {flight_id} with departure date {departure_date}")
    print(f"Filters rows to find flight {flight_id} with departure date {departure_date} and selects seats_available column")
    print(f"Seats available for flight {flight_id} with departure date {departure_date}:")
    available_seats(flight_id, departure_date)

# description of user story
print("US10: show how many seats are left in a specified flight with given departure date\n")

#print tables before querying
print("Flight table before querying:")
print("Flight Table:")
print_table("Flight", ['flight_id', 'departure_date', 'departure_airport', 'destination_airport', 'departure_time', 'arrival_time', 'seats_available', 'airline_id'])

#execute user stories
show_available_seats("AA9803", "2024-11-21")
show_available_seats("UA6214", "2024-11-21")
show_available_seats("NK3785", "2024-11-23")

# Run python script with the following command:
    # % python us10-provide-seating_availability-simple-operational.py

