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
* Complex Operational US: Find Lowest Fare

   As a:  Traveler
 I want:  To find the cheapest flight
So That:  I spend the least amount of money on travel expenses
'''
print(us)

# US3 -- Find lowest fare
def lowest_fare(a_from, a_to, date): # params of flight (i.e. to/from airport, date)
    
    tmpl = ''' 
        WITH lowest_fare AS (SELECT MIN(o.price) AS fare
                               FROM Offer AS o
                               JOIN Flight_Offer AS fl
                                 ON o.offer_id = fl.offer_id
                               JOIN Flight AS f
                                 ON fl.flight_id = f.flight_id
                              WHERE f.departure_airport = %s AND f.destination_airport = %s 
                                                             AND f.departure_date = CAST(%s AS DATE))

        SELECT o.price AS Fare, f.flight_id, f.departure_time, f.arrival_time, f.seats_available, f.airline_id
          FROM Offer AS o
          JOIN Flight_Offer AS fl
            ON o.offer_id = fl.offer_id
          JOIN Flight AS f
            ON fl.flight_id = f.flight_id
         WHERE f.departure_airport = %s AND f.destination_airport = %s 
                                        AND f.departure_date = CAST(%s AS DATE)
                                        AND o.price = (SELECT fare FROM lowest_fare)
    '''
    cmd = cur.mogrify(tmpl, (a_from, a_to, date, a_from, a_to, date))
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    if rows:
          columns = ['Fare', 'flight_id', 'departure_time', 'arrival_time', 'seats_available', 'airline_id']
          show_table(rows, cols=columns)
    else:
        print(f"No flights found from {a_from} to {a_to} on {date}.") # insert parameters

# helper function to demonstrate US3
def print_cheapest(from_loc, to_loc, day):
    print(f"\nExecuting user story from", from_loc, "to", to_loc, "on", day)
    print(f"Joins Offer, Flight, and Flight_Offer tables, filters rows from", from_loc, "to", to_loc, "on", day)
    print(f"Cheapest flight from {from_loc} to {to_loc} on {day}:")
    lowest_fare(from_loc, to_loc, day)

# description of user story
print("US3: finds the lowest fare given departure and destination airports and a date\n")

#print tables before querying
print("Offer, Flight_Offer, and Flight tables before querying:")
print("Offer Table:")
print_table("Offer", ['offer_id', 'price'])
print("Flight_Offer Table:")
print_table("Flight_Offer", ['offer_id', 'flight_id', 'departure_date'])
print("Flight Table:")
print_table("Flight", ['flight_id', 'departure_date', 'departure_airport', 'destination_airport', 'departure_time', 'arrival_time', 'seats_available', 'airline_id'])

#execute user stories
print_cheapest("PIT","NYC","11/19/2024")
print_cheapest("PIT","LAX","11/24/2024")
print_cheapest("PIT","DEN","11/24/2024")

# Run python script with the following command:
    # % python us3-find-lowest_fare-complex-operational.py