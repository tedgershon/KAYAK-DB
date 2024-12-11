-- show contents of all tables in the database
-- explain what data is being displayed using echo statements

\c project

\echo "Leg Table: contains information about a particular leg in a search that a user makes"
SELECT * from Leg;

\echo "Leg_in_Search Table: provides information about which legs are in a main search, like how a multi-city trip could consist of 3 legs"
SELECT * from Leg_in_Search;

\echo "Main_Search Table: contains general information about a search that a user makes"
SELECT * from Main_Search;

\echo "Traveler Table: contains IDs to uniquely identify each traveler"
SELECT * from Traveler;

\echo "Review Table: contains reviews provided for airlines"
SELECT * from Review;

\echo "Airline Table: contains airline names and their IDs"
SELECT * from Airline;

\echo "Registered_User Table: contains information about registered users"
SELECT * from Registered_User;

\echo "Guest_User Table: contains information about guest users"
SELECT * from Guest_User;

\echo "Price_Alert Table: contains Price Alerts a specific user has created for a specific offer, also contains a value price drop which is the difference between the current price (if lower) and the initial price, so price drop is initialized to 0 when a Price Alert is created"
SELECT * from Price_Alert;

\echo "Flight Table: contains flights that are actually offered by airlines, where flights make up an offer"
SELECT * from Flight;

\echo "Flight_Offer Table: provides information about which flights are in an offer"
SELECT * from Flight_Offer;

\echo "Offer Table: An assumption is that no bookings are made directly through Kayak. Kayak shows offers (which are like potential bookings). An offer consists of flights and has a price associated with it."
SELECT * from Offer;

\echo "Selection Table: A user can select to view an offer (a Selection) and are redirected to the travel site to actually book the offer. A selection is a measure of interest in the offer."
SELECT * from Selection;

-- % psql -d postgres -U isdb -f show_all.sql