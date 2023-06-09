import tkinter as tk
from tkinter import ttk
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Symptomy chorób
choroba_serca = [
 'zawał serca',
 'arytmia',
 'zakrzepica',
 'ból w klatce piersiowej',
 'objawy choroby wieńcowej']

objawy_grypy = [
    'gorączka',
    'ból gardła',
    'katar',
    'kaszel',
    'objawy grypy'
]

objawy_alzheimera = [
    'utrata pamięci',
    'dezorientacja',
    'dezorganizacja',
    'objawy alzheimera'
]

objawy_cukrzycy = [
    'częste oddawanie moczu',
    'pragnienie',
    'nieuzasadniona utrata wagi',
    'wzmożony apetyt',
    'objawy cukrzycy'
]

objawy_astmy = [
    'duszność',
    'objawy astmy',
    'kaszel',
    'uczucie ściskania w klatce piersiowej',
    'trudności w oddychaniu'
]

objawy_raka_piersi = [
    'guzek w piersi',
    'wydzielina lub wciągnięcie brodawki sutkowej',
    'marskość lub pomarszczenie skóry',
    'objawy raka piersi'
]

objawy_raka_pluc = [
    'utrzymujący się kaszel',
    'kaszel z krwią',
    'chrypka',
    'duszność',
    'objawy raka płuc'
]

# Funkcje obsługujące zdarzenia
def pobierz_dane():
    wybrana_choroba = choroba_combobox.get()

    if wybrana_choroba.lower() == 'choroba serca':
        objawy = choroba_serca
        nazwa_pliku = 'output_choroba_serca.csv'
    elif wybrana_choroba.lower() == 'grypa':
        objawy = objawy_grypy
        nazwa_pliku = 'output_objawy_grypy.csv'
    elif wybrana_choroba.lower() == 'alzheimer':
        objawy = objawy_alzheimera
        nazwa_pliku = 'output_alzheimer.csv'
    elif wybrana_choroba.lower() == 'cukrzyca':
        objawy = objawy_cukrzycy
        nazwa_pliku = 'output_objawy_cukrzycy.csv'
    elif wybrana_choroba.lower() == 'astma':
        objawy = objawy_astmy
        nazwa_pliku = 'output_objawy_astmy.csv'
    elif wybrana_choroba.lower() == 'rak piersi':
        objawy = objawy_raka_piersi
        nazwa_pliku = 'output_objawy_raka_piersi.csv'
    elif wybrana_choroba.lower() == 'rak płuc':
        objawy = objawy_raka_pluc
        nazwa_pliku = 'output_objawy_raka_pluc.csv'
    else:
        return

    pytrends = TrendReq(hl='pl-PL', tz=360)
    pytrends.build_payload(objawy, timeframe='today 5-y', geo='PL')

    data = pytrends.interest_over_time()

    data.reset_index(inplace=True)

    output = pd.melt(data, id_vars=['date', 'isPartial'], value_vars=objawy, var_name='NAZWA_OBJAWU', value_name='WARTOSC_WYSZUKIWANIA')
    output['date'] = pd.to_datetime(output['date'])

    output = output.rename(columns={'date': 'DATA', 'total': 'TOTAL'})
    output = output[['DATA', 'NAZWA_OBJAWU', 'WARTOSC_WYSZUKIWANIA', 'isPartial']]
    output = output.sort_values(by=['DATA', 'NAZWA_OBJAWU'], ascending=[True, True])

    output.to_csv(nazwa_pliku)
    komunikat_label.config(text=f"Plik został pobrany: {nazwa_pliku}")

    # Generowanie wykresu liniowego
    fig, ax = plt.subplots(figsize=(8, 6))
    for objaw in objawy:
        ax.plot(data['date'], data[objaw], label=objaw)
    ax.set(xlabel='Data', ylabel='Wartość wyszukiwań', title='Trend wyszukiwań objawów')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Interfejs użytkownika
root = tk.Tk()
root.title('Pobieranie trendów z Google')

# Opis programu
opis_programu = "Program pobiera trendy wyszukiwania objawów różnych chorób z Google Trends. Wybierz chorobę z listy rozwijanej i kliknij przycisk 'Pobierz dane', aby pobrać dane dotyczące trendów wyszukiwania dla wybranej choroby."

# Tworzenie etykiety opisu programu
opis_label = ttk.Label(root, text=opis_programu, wraplength=400)
opis_label.pack()

choroba_label = ttk.Label(root, text='Wybierz chorobę:')
choroba_label.pack()

# Tworzenie listy rozwijanej
choroba_combobox = ttk.Combobox(root, values=['Choroba serca', 'Grypa', 'Alzheimer', 'Cukrzyca', 'Astma', 'Rak piersi', 'Rak płuc'])
choroba_combobox.pack()

# Tworzenie przycisku
pobierz_button = ttk.Button(root, text='Pobierz dane', command=pobierz_dane)
pobierz_button.pack()

# Tworzenie etykiety na komunikat
komunikat_label = ttk.Label(root, text='')
komunikat_label.pack()

# Uruchamianie pętli zdarzeń
root.mainloop()
