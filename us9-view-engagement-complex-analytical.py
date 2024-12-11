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
* Complex Analytical US: View Engagement

   As a:  Airline
 I want:  To view traffic that comes from KAYAK redirections and my performance compared to competitors
So That:  I can view how much my company is profiting from using KAYAK and make informed decisions based on traveler demand/engagement
'''
print(us)

# US9 -- View engagement
def engagement(airline_name):
    tmpl = ''' 
        WITH engagement_summary AS (SELECT a.name as airline_name, 
                                           count(s.selection_id) as selection_num, 
                                           ROUND(count(s.selection_id)/sum(count(s.selection_id)) over () * 100, 2) as selection_percentage, 
                                           dense_rank() over w2 as rank
                                      FROM Airline as a 
                                      LEFT JOIN Flight as f 
                                        ON f.airline_id = a.airline_id
                                      LEFT JOIN Flight_Offer as f_in_o 
                                        ON f_in_o.flight_id = f.flight_id
                                      LEFT JOIN Selection as s 
                                        ON s.offer_id = f_in_o.offer_id
                                     GROUP BY a.airline_id
                                    WINDOW w2 as (ORDER BY count(s.selection_id) DESC))

       SELECT airline_name, selection_num, selection_percentage, rank
         FROM engagement_summary 
        WHERE airline_name = %s
    '''
    cmd = cur.mogrify(tmpl, (airline_name,))
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    columns = ["Airline", "Total # of Selections", "Selection Share %", "Rank"]
    show_table(rows, cols=columns)

# helper functions to demonstrate US9
def airline_from_selection():
    print("\nShows which airline is associated with each selection:")
    tmpl = ''' 
        SELECT s.selection_id, a.name
          FROM Selection as s
          JOIN Flight_Offer as f_in_o 
            ON s.offer_id = f_in_o .offer_id
          JOIN Flight as f
            ON f_in_o.flight_id = f.flight_id
          JOIN Airline as a
            ON f.airline_id = a.airline_id
         ORDER BY s.selection_id
    '''
    cmd = cur.mogrify(tmpl)
    cur.execute(cmd)
    rows = cur.fetchall()
    columns = ["Selection", "Airline"]
    show_table(rows, cols=columns)

def engagement_summary(): 
    print("\nTable with total and relative engagement numbers for all airlines:")
    tmpl = ''' 
        SELECT a.name, 
               count(s.selection_id), 
               ROUND(count(s.selection_id)/sum(count(s.selection_id)) over () * 100, 2), 
               dense_rank() over w2
          FROM Airline as a 
          LEFT JOIN Flight as f 
            ON f.airline_id = a.airline_id
          LEFT JOIN Flight_Offer as f_in_o 
            ON f_in_o.flight_id = f.flight_id
          LEFT JOIN Selection as s 
            ON s.offer_id = f_in_o.offer_id
         GROUP BY a.airline_id
        WINDOW w2 as (ORDER BY count(s.selection_id) DESC)
    '''
    cmd = cur.mogrify(tmpl)
    cur.execute(cmd)
    rows = cur.fetchall()
    columns = ["Airline", "Total # of Selections", "Selection Share %", "Rank"]
    show_table(rows, cols=columns)

def show_engagement(airline_name):
    print(f"\nExecuting user story for {airline_name}")
    print(f"Creates a temporary table (engagement summary) with engagement numbers for all airlines using window functions then filters engagement summary table for {airline_name}")
    print(f"{airline_name} engagement:")
    engagement(airline_name)

# description of user story
print("US9: shows total and relative traffic and engagement for a specific airline\n")

# print tables before querying
print("Selection, Flight_Offer, Flight, and Airline tables before querying:")
print("Selection Table:")
print_table("Selection", ['selection_id', 'time_of_selection', 'offer_id', 'traveler_id'])
print("Flight_Offer Table:")
print_table("Flight_Offer", ['offer_id', 'flight_id', 'departure_date'])
print("Flight Table:")
print_table("Flight", ['flight_id', 'departure_date', 'departure_airport', 'destination_airport', 'departure_time', 'arrival_time', 'seats_available', 'airline_id'])
print("Airline Table:")
print_table("Airline", ['airline_id', 'name'])

# gives some more descriptive steps in the query
airline_from_selection()
engagement_summary()

#execute user stories
show_engagement("American Airlines")
show_engagement("United Airlines")
show_engagement("Spirit Airlines")
show_engagement("Delta Airlines")
show_engagement("Alaska Airlines")

# Run python script with the following command:
    # % python us9-view-engagement-complex-analytical.py