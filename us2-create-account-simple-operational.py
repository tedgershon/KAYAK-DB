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
* Simple Operational US: Create Account

   As a:  Traveler
 I want:  To create an account profile
So That:  I can keep track of searches and prices, save flights, and get member-only deals
'''
print(us)

# US2 -- Create account
def create_account(new_name, new_email):

    # find next traveler_id via query on Traveler table (COALESCE used to return 0 from an empty table)
    next_id = '''SELECT COALESCE(MAX(traveler_id), 0)+1 FROM Traveler'''
    cur.execute(next_id)
    new_traveler_id = cur.fetchone()[0]
    # check if new_name, new_email combo already exists and prevent add if so
    check_duplicate = '''SELECT COUNT(traveler_id)
                           FROM Registered_User
                          WHERE name ILIKE %s AND email ILIKE %s'''
    dup = cur.mogrify(check_duplicate, (new_name, new_email))
    cur.execute(dup)
    repeat = cur.fetchone()[0]

    if(repeat == 0):
        # insert account into Traveler and Registered_User tables
        tmpl = '''
        INSERT INTO Traveler (traveler_id)
        VALUES (%s);
        INSERT INTO Registered_User (name, email, traveler_id)
        VALUES (%s, %s, %s)
        '''
        cmd = cur.mogrify(tmpl, (new_traveler_id, new_name, new_email, new_traveler_id))
        # print query code
        print_cmd(cmd)
        # execute query
        cur.execute(cmd)

    # rather than printing query results, print updated Registered_User table
    print_table("Registered_User", ['name', 'email', 'traveler_id'])

# helper function to demonstrate US2
def add_user(name, email): # insert added user params in this function argument
    print(f"\nExecuting user story for", name, "with email", email) # insert user name here
    print(f"Adds a new account to the Registered_User table, generating a unique traveler_id for {name} ({email})\n") # insert user name here
    print(f"Registered_User Table before {name} ({email}) added:")
    print_table("Registered_User", ['name', 'email', 'traveler_id']) # print Registered_User table before create_account() execution
    print(f"Traveler Table:")
    print_table("Traveler", ['traveler_id'])
    print(f"\nRegistered_User Table after {name} ({email}) added:")
    create_account(name, email) # Registered_User table automatically printed via create_account()
    print(f"Traveler Table:")
    print_table("Traveler", ['traveler_id'])

# description of user story
print("US2: creates a new account and unique traveler_id given name and email parameters")

#no need to print table before querying, as this should be done immediately before query to show effect of create_account()

#execute user stories
add_user("Clarence Choy", "czmoney@example.com")
add_user("Jonathan Gu", "jbg2@example.com")

# Run python script with the following command:
    # % python us2-create-account-simple-operational.py