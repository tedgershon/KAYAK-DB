\c postgres
DROP database if EXISTS project;

CREATE database project;
\c project

-- load tables from Vertabelo
\i create.SQL

-- copy data from CSV files
\copy Airline(airline_id, name) FROM data/airlines.csv csv header;
\copy Flight(flight_id, departure_date, departure_airport, destination_airport, departure_time, arrival_time, seats_available, airline_id) FROM data/flights.csv csv header;
\copy Offer(offer_id, price) FROM data/offers.csv csv header;
\copy Flight_Offer(offer_id, flight_id, departure_date) FROM data/flight_offers.csv csv header;
\copy Traveler(traveler_id) FROM data/travelers.csv csv header;
\copy Guest_User(ip_address, timestamp, traveler_id) FROM data/guest_users.csv csv header;
\copy Leg(search_id, from_location, to_location, departure_date, class) FROM data/legs.csv csv header;
\copy Main_Search(main_search_id, trip_type, num_travelers, date_searched, time_searched, traveler_id) FROM data/main_searches.csv csv header;
\copy Leg_in_Search(search_id, main_search_id) FROM data/legs_in_search.csv csv header;
\copy Price_Alert(traveler_id, offer_id, price_drop) FROM data/price_alerts.csv csv header;
\copy Registered_User(name, email, traveler_id) FROM data/registered_users.csv csv header;
\copy Review(review_id, rating, comment, airline_id, traveler_id) FROM data/reviews.csv csv header;
\copy Selection(selection_id, time_of_selection, offer_id, traveler_id) FROM data/selections.csv csv header;

-- Trigger Function: fn_price_alert
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
END $$;

-- Trigger: tr_price_alert()
DROP TRIGGER IF EXISTS tr_price_alert ON Offer; 
CREATE TRIGGER tr_price_alert
AFTER UPDATE OF price ON Offer 
FOR EACH ROW 
EXECUTE FUNCTION fn_price_alert()

-- run user stories from seed.zip file with the following command:
    -- % unzip seed.zip
    -- % cd seed
    -- % psql -d postgres -U isdb -f initialize.sql
    -- % psql -d postgres -U isdb -f show_all.sql
    -- % python us1-filter-airlines-complex-operational.py
    -- % python us2-create-account-simple-operational.py
    -- % python us3-find-lowest_fare-complex-operational.py
    -- % python us4-find-quickest_trip-simple-analytical.py
    -- % python us5-find-popular_searches-complex-analytical.py
    -- % python us6-find-popular_airlines-complex-analytical.py
    -- % python us7-receive-price_alert-complex-operational.py
    -- % python us8-view-airline_reviews-complex-operational.py
    -- % python us9-view-engagement-complex-analytical.py
    -- % python us10-provide-seating_availability-simple-operational.py