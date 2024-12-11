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
* Complex Operational US: Receive Price Alert

   As a:  Registered Traveler
 I want:  To receive Price Alerts through email about an offer
So That:  I can book when there is a noteworthy price drop to save money
'''
print(us)

# US7 -- Receive Price Alert
def print_price_alert():
    print("Here are the trigger function and trigger defined in initialize.sql:")
    tmpl = ''' 
        CREATE OR REPLACE FUNCTION fn_price_alert()
        RETURNS trigger
        LANGUAGE plpgsql AS
        $$
        DECLARE 
            old_price_drop NUMERIC;
        BEGIN 
            SELECT price_drop 
              INTO old_price_drop 
              FROM Price_Alert 
             WHERE offer_id = new.offer_id;
                if old.price > new.price then
                    UPDATE Price_Alert
                    SET price_drop = old_price_drop + (old.price - new.price)
                    WHERE (offer_id = new.offer_id);
               end if;
            return null;
        END $$
    '''
    cmd = cur.mogrify(tmpl)
    # print query code
    print_cmd(cmd)

    tmpl = '''
        DROP TRIGGER IF EXISTS tr_price_alert ON Offer; 
        CREATE TRIGGER tr_price_alert
        AFTER UPDATE OF price ON Offer
        FOR EACH ROW
        EXECUTE FUNCTION fn_price_alert()
    '''
    cmd = cur.mogrify(tmpl)
    # print query code
    print_cmd(cmd)

# helpers function to demonstrate US7
# SQL code to execute the event (UPDATE OF Price ON Offer)
def update_offer_price(amount, offer_id):
    print("Here is the SQL code of the event:")
    tmpl = ''' 
        UPDATE Offer
           SET price = price - %s
         WHERE offer_id = %s
    '''
    cmd = cur.mogrify(tmpl, (amount, offer_id))
    # print query code
    print_cmd(cmd)
    # execute query
    cur.execute(cmd)

def show_offers(offer_id):
    tmpl = ''' 
        SELECT offer_id, price
          FROM Offer
         WHERE offer_id = %s
    '''
    cmd = cur.mogrify(tmpl, (offer_id,))
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    columns = ["Offer ID", "Price"]
    show_table(rows, cols=columns)
    
def show_price_alerts(offer_id):
    tmpl = ''' 
        SELECT traveler_id, offer_id, price_drop
          FROM Price_Alert
         WHERE offer_id = %s
    '''
    cmd = cur.mogrify(tmpl, (offer_id,))
    # execute query
    cur.execute(cmd)
    rows = cur.fetchall()
    columns = ["Traveler ID", "Offer ID", "Price Drop"]
    show_table(rows, cols=columns)

def show_price_alert(offer_id):
    print(f"\nExecuting user story for a price drop on offer {offer_id}")
    # call the trigger function
    print(f"\nValues before price of offer {offer_id} changes:")
    # show tables before price change
    print("Offer Table:")
    show_offers(offer_id)
    print("Price_Alert Table:")
    show_price_alerts(offer_id)
    # make price change
    print(f"\nDecreasing the price of offer {offer_id} by $10, causing the trigger function to execute")
    update_offer_price(10, offer_id)
    print(f"The trigger function updates each price alert created for offer {offer_id} to have a price drop of $10")
    print(f"\nValues after price of offer {offer_id} changes:")
    #show tables after price change
    print("Offer Table:")
    show_offers(offer_id)
    print("Price_Alert Table:")
    show_price_alerts(offer_id)
    print(f"\nIf we decrease the price of offer {offer_id} by $20, the trigger function will execute again")
    update_offer_price(20, offer_id)
    print(f"The trigger function updates each price alert created for offer {offer_id} to have a price drop of $30 (the difference from the original price)")
    print(f"\nValues after price of offer {offer_id} changes again:")
    print("Offer Table:")
    show_offers(offer_id)
    print("Price_Alert Table:")
    show_price_alerts(offer_id)

# description of user story
print("US7: update price alert users have created for a specific offer when the price of that offer drops\n")
print_price_alert()

#print tables before querying
print("Offer and Price_Alert tables before querying:")
print("Offer Table:")
print_table("Offer", ['offer_id', 'price'])
print("Price_Alert Table:")
print_table("Price_Alert", ['traveler_id', 'offer_id', 'price_drop'])

#execute user stories
show_price_alert(1)
show_price_alert(3)

# Run python script with the following command:
    # % python us7-receive-price_alert-complex-operational.py