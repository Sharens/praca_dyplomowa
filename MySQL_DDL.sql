----------------------------------------------------------------------
-- Utworzenie bazy danych 
----------------------------------------------------------------------

CREATE DATABASE praca_dyplomowa

----------------------------------------------------------------------
--Tworzenie tabeli z outputem dla wyszukiwań choroby wieńcowej
----------------------------------------------------------------------
CREATE TABLE STG_DIS_Choroba_Wiencowa (
	DATA  date,
    NAZWA_OBJAWU varchar(100),
    WARTOSC_WYSZUKIWANIA integer,
    TOTAL integer,
    isPartial varchar(10)
);