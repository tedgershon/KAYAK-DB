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
* Complex Analytical US: Find Popular Searches

   As a:  KAYAK Manager
 I want:  To find which routes are currently the most searched
So That:  I can suggest trending recommendations to travelers
'''
print(us)

# US5 -- Find popular searches
def popular_searches(date):
    # filter by given date and date before given date
    tmpl = ''' 
        WITH counts AS (SELECT l.to_location as destination, count(l.to_location) as num_of_searches
                          FROM Main_Search as m 
                          JOIN Leg_in_Search as l_in_m 
                            ON m.main_search_id = l_in_m.main_search_id
                          JOIN Leg as l 
                            ON l_in_m.search_id = l.search_id
                         WHERE (m.date_searched = TO_DATE(%s, 'MM/DD/YY')) OR (m.date_searched = (TO_DATE(%s, 'MM/DD/YY') - INTERVAL '1' DAY))  
                         GROUP BY l.to_location)
        SELECT destination, num_of_searches
          FROM counts
         WHERE num_of_searches = (SELECT max(num_of_searches) FROM counts)
    '''
    cmd = cur.mogrify(tmpl, (date, date))
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    columns = ["Popular Destination", "# of Searches"]
    show_table(rows, cols=columns)

# helper function to demonstrate US5
def find_popular_searches(date):
    print(f"\nExecuting user story for {date}")
    print(f"Joins Leg, Leg_in_Search, and Main_Search tables, filters rows by searched for on {date} and the day before")
    print(f"Trending destination(s) for {date}:")
    popular_searches(date)

# description of user story
print("US5: finds top trending destination(s) (most searched in past 2 days)\n")

#print tables before querying
print("Main_Search, Leg_in_Search, and Leg tables before querying:")
print("Main_Search Table:")
print_table("Main_Search", ['main_search_id', 'trip_type', 'num_travelers', 'date_searched', 'time_searched', 'traveler_id'])
print("Leg_in_Search Table:")
print_table("Leg_in_Search", ['search_id', 'main_search_id'])
print("Leg Table:")
print_table("Leg", ['search_id', 'from_location', 'to_location', 'departure_date', 'class'])

#execute user stories
find_popular_searches("11/20/24")
find_popular_searches("11/21/24")
find_popular_searches("11/22/24")

# Run python script with the following command:
    # % python us5-find-popular_searches-complex-analytical.py