-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-12-07 21:21:13.473

-- tables
-- Table: Airline
CREATE TABLE Airline (
    airline_id int  NOT NULL,
    name text  NOT NULL,
    CONSTRAINT Airline_pk PRIMARY KEY (airline_id)
);

-- Table: Flight
CREATE TABLE Flight (
    flight_id text  NOT NULL,
    departure_date date  NOT NULL,
    departure_airport text  NOT NULL,
    destination_airport text  NOT NULL,
    departure_time time  NOT NULL,
    arrival_time time  NOT NULL,
    seats_available int  NOT NULL,
    airline_id int  NOT NULL,
    CONSTRAINT Flight_pk PRIMARY KEY (flight_id,departure_date)
);

-- Table: Flight_Offer
CREATE TABLE Flight_Offer (
    offer_id int  NOT NULL,
    flight_id text  NOT NULL,
    departure_date date  NOT NULL,
    CONSTRAINT Flight_Offer_pk PRIMARY KEY (offer_id,flight_id,departure_date)
);

-- Table: Guest_User
CREATE TABLE Guest_User (
    ip_address text  NOT NULL,
    timestamp timestamp  NOT NULL,
    traveler_id int  NOT NULL,
    CONSTRAINT Guest_User_pk PRIMARY KEY (traveler_id)
);

-- Table: Leg
CREATE TABLE Leg (
    search_id int  NOT NULL,
    from_location text  NOT NULL,
    to_location text  NOT NULL,
    departure_date date  NOT NULL,
    class text  NOT NULL,
    CONSTRAINT Leg_pk PRIMARY KEY (search_id)
);

-- Table: Leg_in_Search
CREATE TABLE Leg_in_Search (
    search_id int  NOT NULL,
    main_search_id int  NOT NULL,
    CONSTRAINT Leg_in_Search_pk PRIMARY KEY (search_id,main_search_id)
);

-- Table: Main_Search
CREATE TABLE Main_Search (
    main_search_id int  NOT NULL,
    trip_type text  NOT NULL,
    num_travelers int  NOT NULL,
    date_searched date  NOT NULL,
    time_searched time  NOT NULL,
    traveler_id int  NOT NULL,
    CONSTRAINT Main_Search_pk PRIMARY KEY (main_search_id)
);

-- Table: Offer
CREATE TABLE Offer (
    offer_id int  NOT NULL,
    price decimal(8,2)  NOT NULL,
    CONSTRAINT Offer_pk PRIMARY KEY (offer_id)
);

-- Table: Price_Alert
CREATE TABLE Price_Alert (
    traveler_id int  NOT NULL,
    offer_id int  NOT NULL,
    price_drop decimal(8,2)  NOT NULL,
    CONSTRAINT Price_Alert_pk PRIMARY KEY (offer_id,traveler_id)
);

-- Table: Registered_User
CREATE TABLE Registered_User (
    name text  NOT NULL,
    email text  NOT NULL,
    traveler_id int  NOT NULL,
    CONSTRAINT Registered_User_pk PRIMARY KEY (traveler_id)
);

-- Table: Review
CREATE TABLE Review (
    review_id int  NOT NULL,
    rating int  NOT NULL,
    comment text  NOT NULL,
    airline_id int  NOT NULL,
    traveler_id int  NOT NULL,
    CONSTRAINT Review_pk PRIMARY KEY (review_id)
);

-- Table: Selection
CREATE TABLE Selection (
    selection_id int  NOT NULL,
    time_of_selection time  NOT NULL,
    offer_id int  NOT NULL,
    traveler_id int  NOT NULL,
    CONSTRAINT Selection_pk PRIMARY KEY (selection_id,time_of_selection)
);

-- Table: Traveler
CREATE TABLE Traveler (
    traveler_id int  NOT NULL,
    CONSTRAINT Traveler_pk PRIMARY KEY (traveler_id)
);

-- foreign keys
-- Reference: Flight_Airline (table: Flight)
ALTER TABLE Flight ADD CONSTRAINT Flight_Airline
    FOREIGN KEY (airline_id)
    REFERENCES Airline (airline_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Flight_Offer_Flight (table: Flight_Offer)
ALTER TABLE Flight_Offer ADD CONSTRAINT Flight_Offer_Flight
    FOREIGN KEY (flight_id, departure_date)
    REFERENCES Flight (flight_id, departure_date)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Flight_Offer_Offer (table: Flight_Offer)
ALTER TABLE Flight_Offer ADD CONSTRAINT Flight_Offer_Offer
    FOREIGN KEY (offer_id)
    REFERENCES Offer (offer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Guest_User_Traveler (table: Guest_User)
ALTER TABLE Guest_User ADD CONSTRAINT Guest_User_Traveler
    FOREIGN KEY (traveler_id)
    REFERENCES Traveler (traveler_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Leg_in_Search_Leg (table: Leg_in_Search)
ALTER TABLE Leg_in_Search ADD CONSTRAINT Leg_in_Search_Leg
    FOREIGN KEY (search_id)
    REFERENCES Leg (search_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Leg_in_Search_Main_Search (table: Leg_in_Search)
ALTER TABLE Leg_in_Search ADD CONSTRAINT Leg_in_Search_Main_Search
    FOREIGN KEY (main_search_id)
    REFERENCES Main_Search (main_search_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Main_Search_Traveler (table: Main_Search)
ALTER TABLE Main_Search ADD CONSTRAINT Main_Search_Traveler
    FOREIGN KEY (traveler_id)
    REFERENCES Traveler (traveler_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Offer_Price_Alert (table: Price_Alert)
ALTER TABLE Price_Alert ADD CONSTRAINT Offer_Price_Alert
    FOREIGN KEY (offer_id)
    REFERENCES Offer (offer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Registered_User_Traveler (table: Registered_User)
ALTER TABLE Registered_User ADD CONSTRAINT Registered_User_Traveler
    FOREIGN KEY (traveler_id)
    REFERENCES Traveler (traveler_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Review_Airline (table: Review)
ALTER TABLE Review ADD CONSTRAINT Review_Airline
    FOREIGN KEY (airline_id)
    REFERENCES Airline (airline_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Selection_Offer (table: Selection)
ALTER TABLE Selection ADD CONSTRAINT Selection_Offer
    FOREIGN KEY (offer_id)
    REFERENCES Offer (offer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Selection_Traveler (table: Selection)
ALTER TABLE Selection ADD CONSTRAINT Selection_Traveler
    FOREIGN KEY (traveler_id)
    REFERENCES Traveler (traveler_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Traveler_Price_Alert (table: Price_Alert)
ALTER TABLE Price_Alert ADD CONSTRAINT Traveler_Price_Alert
    FOREIGN KEY (traveler_id)
    REFERENCES Traveler (traveler_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Traveler_Review (table: Review)
ALTER TABLE Review ADD CONSTRAINT Traveler_Review
    FOREIGN KEY (traveler_id)
    REFERENCES Traveler (traveler_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

