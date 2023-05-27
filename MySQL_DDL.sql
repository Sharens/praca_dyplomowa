----------------------------------------------------------------------
-- Utworzenie bazy danych 
----------------------------------------------------------------------

CREATE DATABASE praca_dyplomowa

----------------------------------------------------------------------
-- Tworzenie tabeli z outputem dla wyszukiwań choroby wieńcowej
----------------------------------------------------------------------
CREATE TABLE STG_DIS_Choroba_Wiencowa (
	DATA  date,
    NAZWA_OBJAWU varchar(100),
    WARTOSC_WYSZUKIWANIA integer,
    TOTAL integer,
    isPartial varchar(10)
);

----------------------------------------------------------------------
-- Ładowanie danych do bazy danych
----------------------------------------------------------------------
LOAD DATA INFILE "C:\Users\lenovoo\Downloads\output.csv"
INTO TABLE stg_dis_choroba_wiencowa
FIELDS TERMINATED BY ','