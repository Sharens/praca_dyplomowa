import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pytrends.request import TrendReq
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import base64

# Symptomy chorób
symptomy = {
    'choroba_serca': [
        'zawał serca',
        'arytmia',
        'zakrzepica',
        'ból w klatce piersiowej',
        'objawy choroby wieńcowej'
    ],
    'objawy_grypy': [
        'gorączka',
        'ból gardła',
        'katar',
        'kaszel',
        'objawy grypy'
    ],
    'objawy_alzheimera': [
        'utrata pamięci',
        'dezorientacja',
        'dezorganizacja',
        'objawy alzheimera'
    ],
    'objawy_cukrzycy': [
        'częste oddawanie moczu',
        'pragnienie',
        'nieuzasadniona utrata wagi',
        'wzmożony apetyt',
        'objawy cukrzycy'
    ],
    'objawy_astmy': [
        'duszność',
        'objawy astmy',
        'kaszel',
        'uczucie ściskania w klatce piersiowej',
        'trudności w oddychaniu'
    ],
    'objawy_raka_piersi': [
        'guzek w piersi',
        'wydzielina lub wciągnięcie brodawki sutkowej',
        'marskość lub pomarszczenie skóry',
        'objawy raka piersi'
    ],
    'objawy_raka_pluc': [
        'utrzymujący się kaszel',
        'kaszel z krwią',
        'chrypka',
        'duszność',
        'objawy raka płuc'
    ]
}

# Funkcje obsługujące zdarzenia
def pobierz_dane(choroba):
    pytrends = TrendReq(hl='pl-PL', tz=360)
    pytrends.build_payload(choroba, timeframe='all', geo='PL')

    data = pytrends.interest_over_time()

    data.reset_index(inplace=True)

    output = pd.melt(data, id_vars=['date'], value_vars=choroba, var_name='NAZWA_OBJAWU',
                     value_name='WARTOSC_WYSZUKIWANIA')
    output['date'] = pd.to_datetime(output['date'])

    output = output.rename(columns={'date': 'DATA', 'total': 'TOTAL'})
    output = output[['DATA', 'NAZWA_OBJAWU', 'WARTOSC_WYSZUKIWANIA']]
    output = output.sort_values(by=['DATA', 'NAZWA_OBJAWU'], ascending=[True, True])

    return output

def generuj_wykresy(data):
    fig1 = px.line(data, x='DATA', y='WARTOSC_WYSZUKIWANIA', color='NAZWA_OBJAWU',
                   title='Trend wyszukiwań symptomów')
    sum_objawy = data.groupby('DATA')['WARTOSC_WYSZUKIWANIA'].sum().reset_index()
    fig2 = px.line(x=sum_objawy['DATA'], y=sum_objawy['WARTOSC_WYSZUKIWANIA'])
    fig2.update_layout(
        title='Suma wyszukiwań dla wszystkich objawów',
        xaxis_title='Data',
        yaxis_title='Suma wyszukiwań'
    )

    return fig1, fig2

# Interfejs użytkownika
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Pobieranie trendów z Google'),
    html.H2('Opis programu'),
    html.P(
        "Program pobiera trendy wyszukiwania objawów różnych chorób z Google Trends. Wybierz chorobę z listy rozwijanej i "
        "kliknij przycisk 'Pobierz dane .csv', aby pobrać dane dotyczące trendów wyszukiwania dla wybranej choroby."
    ),
    html.H3('Wybierz chorobę:'),
    dcc.Dropdown(
        id='choroba-dropdown',
        options=[
            {'label': 'Choroba serca', 'value': 'choroba_serca'},
            {'label': 'Grypa', 'value': 'objawy_grypy'},
            {'label': 'Alzheimer', 'value': 'objawy_alzheimera'},
            {'label': 'Cukrzyca', 'value': 'objawy_cukrzycy'},
            {'label': 'Astma', 'value': 'objawy_astmy'},
            {'label': 'Rak piersi', 'value': 'objawy_raka_piersi'},
            {'label': 'Rak płuc', 'value': 'objawy_raka_pluc'}
        ],
        value=None,
        placeholder='Wybierz chorobę',
        clearable=False
    ),
    html.Button('Pobierz dane .csv', id='pobierz-csv-button', n_clicks=0),
    html.Button('Wygeneruj wykresy', id='wygeneruj-wykresy-button', n_clicks=0),
    html.Div(id='komunikat-output'),
    dcc.Graph(id='wykres1'),
    dcc.Graph(id='wykres2'),
    dcc.Download(id="download-csv")
])

@app.callback(
    Output('komunikat-output', 'children'),
    Output('download-csv', 'data'),
    [Input('pobierz-csv-button', 'n_clicks')],
    [State('choroba-dropdown', 'value')]
)
def pobierz_csv_callback(n_clicks, choroba):
    if n_clicks > 0:
        data = pobierz_dane(symptomy[choroba])
        nazwa_pliku = f'{choroba}.csv'
        data.to_csv(nazwa_pliku, index=False)
        return f"Pobrano dane dla choroby: {choroba}", dict(content=data.to_csv(index=False), filename=nazwa_pliku)
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('wykres1', 'figure'),
    Output('wykres2', 'figure'),
    [Input('wygeneruj-wykresy-button', 'n_clicks')],
    [State('choroba-dropdown', 'value')]
)
def generuj_wykresy_callback(n_clicks, choroba):
    if n_clicks > 0:
        data = pobierz_dane(symptomy[choroba])
        fig1, fig2 = generuj_wykresy(data)
        return fig1, fig2
    else:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)