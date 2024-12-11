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
    print_all = f'''
        SELECT * FROM {table}
    '''
    cur.execute(print_all)
    rows = cur.fetchall()
    show_table(rows, cols)

# connect to project db
conn = psycopg2.connect(database='project', user='isdb') 
conn.autocommit = True
cur = conn.cursor()

# User story definition
us='''
* Complex Operational US: View Airline Reviews

   As a:  Traveler
 I want:  To see airline reviews indicating level of customer satisfaction
So That:  I can inform my travel arrangements with which providers have reliable pricing and good customer service
'''
print(us)

# US8 -- View airline reviews
def show_airline_reviews(airline):
    
    tmpl = ''' 
        SELECT r.review_id, r.rating, r.comment
          FROM Airline as a
          JOIN Review as r
            ON a.airline_id = r.airline_id
         WHERE a.name ILIKE %s
         ORDER BY r.review_id
    '''
    cmd = cur.mogrify(tmpl, (f"%{airline}%",)) # allows %s to work even if partial airline name typed
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    if rows:
          columns = ['Review ID', 'Review Score (0-5)', 'Comment']
          show_table(rows, cols=columns)
    else:
        print(f"No reviews found for airline {airline}.")

# helper function to demonstrate US8
def airline_reviews(airline_name):
    print(f"\nExecuting user story for", airline_name)
    print(f"Joins Airline and Review tables, filters rows where airline name is", airline_name)
    print(f"Reviews for {airline_name}:")
    show_airline_reviews(airline_name)

# description of user story
print("US8: provides reviews for a specified airline\n")

# print tables before querying
print("Airline, Review, and Traveler tables before querying:")
print("Airline Table:")
print_table("Airline", ['airline_id', 'name'])
print("Review Table:")
print_table("Review", ['review_id', 'rating', 'comment', 'airline_id', 'traveler_id'])
print("Traveler Table:")
print_table("Traveler", ['traveler_id'])

# execute user stories
airline_reviews("American Airlines")
airline_reviews("United Airlines")
airline_reviews("Spirit Airlines")
airline_reviews("Delta Airlines")
airline_reviews("Alaska Airlines")

# Run python script with the following command:
    # % python us8-view-airline_reviews-complex-operational.py