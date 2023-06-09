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
-- Tworzenie tabeli z outputem dla wyszukiwań grypy
----------------------------------------------------------------------
CREATE TABLE STG_DIS_Grypa (
	DATA  date,
    NAZWA_OBJAWU varchar(100),
    WARTOSC_WYSZUKIWANIA integer,
    isPartial varchar(10)
);


----------------------------------------------------------------------
-- Tworzenie tabeli z outputem dla wyszukiwań alzheimera
----------------------------------------------------------------------
CREATE TABLE STG_DIS_Alzheimer (
	DATA  date,
    NAZWA_OBJAWU varchar(100),
    WARTOSC_WYSZUKIWANIA integer,
    isPartial varchar(10)
);


----------------------------------------------------------------------
-- Tworzenie tabeli z outputem dla wyszukiwań cukrzycy
----------------------------------------------------------------------
CREATE TABLE STG_DIS_Cukrzyca (
	DATA  date,
    NAZWA_OBJAWU varchar(100),
    WARTOSC_WYSZUKIWANIA integer,
    isPartial varchar(10)
);

----------------------------------------------------------------------
-- Tworzenie tabeli z outputem dla wyszukiwań astmy
----------------------------------------------------------------------
CREATE TABLE STG_DIS_astma (
	DATA  date,
    NAZWA_OBJAWU varchar(100),
    WARTOSC_WYSZUKIWANIA integer,
    isPartial varchar(10)
);

----------------------------------------------------------------------
-- Tworzenie tabeli z outputem dla nowotworu piersi
----------------------------------------------------------------------
CREATE TABLE STG_DIS_nowotwor_piersi (
	DATA  date,
    NAZWA_OBJAWU varchar(100),
    WARTOSC_WYSZUKIWANIA integer,
    isPartial varchar(10)
);

----------------------------------------------------------------------
-- Tworzenie tabeli z outputem dla nowotworu płuc
----------------------------------------------------------------------
CREATE TABLE STG_DIS_nowotwor_pluc (
	DATA  date,
    NAZWA_OBJAWU varchar(100),
    WARTOSC_WYSZUKIWANIA integer,
    isPartial varchar(10)
);


----------------------------------------------------------------------
-- Ładowanie danych do bazy danych
----------------------------------------------------------------------
LOAD DATA INFILE "C:\Users\lenovoo\Downloads\output.csv"
INTO TABLE stg_dis_choroba_wiencowa
FIELDS TERMINATED BY ','