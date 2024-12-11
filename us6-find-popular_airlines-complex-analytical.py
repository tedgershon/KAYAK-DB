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
* Complex Analytical US: Find Popular Airlines

   As a:  KAYAK Manager
 I want:  To view what airlines’ offers receive the most user engagement and selections
So That:  I can share insights with airline partners regarding their user engagement
'''
print(us)

# US6 -- Find popular airlines
def popular_airlines():
    tmpl = ''' 
        SELECT a.name, count(s.traveler_id)
          FROM Selection AS s
          JOIN Flight_Offer AS o
            ON s.offer_id = o.offer_id
          JOIN Flight AS f
            ON o.flight_id = f.flight_id
         RIGHT JOIN Airline AS a
            ON f.airline_id = a.airline_id
         GROUP BY a.airline_id
         ORDER BY count(s.traveler_id) DESC
    '''
    cmd = cur.mogrify(tmpl)
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    columns = ['Airline', 'User Count']
    show_table(rows, cols=columns)

# helper function to demonstrate US6
def airlines():
    print(f"\nExecuting user story for airline popularity")
    print(f"Joins Selection, Flight_Offer, Flight, and Airline tables, groups rows by airline id")
    print(f"Traveler selection breakdown by airline:")
    popular_airlines()

# description of user story
print("US6: provides breakdown of most popular airlines by traveler selections\n")

#print tables before querying
print("Selection, Flight_Offer, Flight, and Airline tables before querying:")
print("Selection Table:")
print_table("Selection", ['selection_id', 'time_of_selection', 'offer_id', 'traveler_id'])
print("Flight_Offer Table:")
print_table("Flight_Offer", ['offer_id', 'flight_id', 'departure_date'])
print("Flight Table:")
print_table("Flight", ['flight_id', 'departure_date', 'departure_airport', 'destination_airport', 'departure_time', 'arrival_time', 'seats_available', 'airline_id'])
print("Airline Table:")
print_table("Airline", ['airline_id', 'name'])

#execute user stories
airlines()

# Run python script with the following command:
    # % python us6-find-popular_airlines-complex-analytical.py