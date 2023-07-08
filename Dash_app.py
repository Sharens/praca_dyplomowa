import pandas as pd
import plotly.express as px
from pytrends.request import TrendReq
from dash import Dash, dash, dcc, html
from dash.dependencies import Input, Output, State
import time


# Słownik objawów chorób
symptomy = {
    'choroba_serca': ['zawał serca', 'arytmia', 'zakrzepica', 'ból w klatce piersiowej', 'objawy choroby wieńcowej'],
    'objawy_grypy': ['gorączka', 'ból gardła', 'katar', 'kaszel', 'objawy grypy'],
    'objawy_alzheimera': ['utrata pamięci', 'dezorientacja', 'dezorganizacja', 'objawy alzheimera'],
    'objawy_cukrzycy': ['częste oddawanie moczu', 'pragnienie', 'nieuzasadniona utrata wagi', 'wzmożony apetyt', 'objawy cukrzycy'],
    'objawy_astmy': ['duszność', 'objawy astmy', 'kaszel', 'uczucie ściskania w klatce piersiowej', 'trudności w oddychaniu'],
    'objawy_raka_piersi': ['guzek w piersi', 'wydzielina lub wciągnięcie brodawki sutkowej', 'marskość lub pomarszczenie skóry', 'objawy raka piersi'],
    'objawy_raka_pluc': ['utrzymujący się kaszel', 'rak pluc objawy']
}

# Funkcja pobierająca dane
def pobierz_dane(choroba):
    pytrends = TrendReq(hl='pl-PL', tz=360)
    pytrends.build_payload(choroba, timeframe='today 7-d', geo='PL')
    data = pytrends.interest_over_time().reset_index()

    time.sleep(60)

    return pd.melt(data, id_vars=['date'], value_vars=choroba, var_name='NAZWA_OBJAWU', value_name='WARTOSC_WYSZUKIWANIA').sort_values(by=['date', 'NAZWA_OBJAWU'])

# Funkcja generująca wykresy
def generuj_wykresy(data):
    fig1 = px.line(data, x='date', y='WARTOSC_WYSZUKIWANIA', color='NAZWA_OBJAWU', title='Trend wyszukiwań symptomów')
    sum_objawy = data.groupby('date')['WARTOSC_WYSZUKIWANIA'].sum().reset_index()
    fig2 = px.line(x=sum_objawy['date'], y=sum_objawy['WARTOSC_WYSZUKIWANIA'], title='Suma wyszukiwań dla wszystkich objawów')
    fig2.update_layout(xaxis_title='Data', yaxis_title='Suma wyszukiwań')

    return fig1, fig2

# Interfejs użytkownika
app = Dash(__name__)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Pobieranie trendów', children=[
            html.H1('Pobieranie trendów z Google'),
            html.H2('Opis programu'),
            html.P("Program pobiera trendy wyszukiwania objawów różnych chorób z Google Trends. Wybierz chorobę z listy rozwijanej i kliknij przycisk 'Pobierz dane .csv', aby pobrać dane dotyczące trendów wyszukiwania dla wybranej choroby."),
            html.H3('Wybierz chorobę:'),
            dcc.Dropdown(id='choroba-dropdown', options=[{'label': key, 'value': key} for key in symptomy.keys()], value=None, placeholder='Wybierz chorobę', clearable=False),
            html.Button('Pobierz dane .csv', id='pobierz-csv-button', n_clicks=0),
            html.Button('Wygeneruj wykresy', id='wygeneruj-wykresy-button', n_clicks=0),
            html.Div(id='komunikat-output'),
            dcc.Graph(id='wykres1'),
            dcc.Graph(id='wykres2'),
            dcc.Download(id="download-csv")
        ]),
        dcc.Tab(label='Dodaj nową chorobę', children=[
            html.H3('Dodaj nową chorobę'),
            dcc.Input(id='nowa-choroba', type='text', placeholder='Nazwa nowej choroby'),
            html.H3('Dodaj symptomy'),
            dcc.Textarea(id='nowe-symptomy', placeholder='Wpisz symptomy, oddzielając je przecinkami'),
            html.Div(style={'height': '10px'}), 
            html.Button('Dodaj nową chorobę', id='dodaj-chorobe-button', n_clicks=0),
            html.Div(id='output-nowa-choroba')
        ])
    ])
])

@app.callback(
    Output('choroba-dropdown', 'options'),
    Output('output-nowa-choroba', 'children'),
    [Input('dodaj-chorobe-button', 'n_clicks')],
    [State('nowa-choroba', 'value'),
     State('nowe-symptomy', 'value')]
)
def dodaj_chorobe_callback(n_clicks, nowa_choroba, nowe_symptomy):
    if n_clicks > 0:
        nowe_symptomy = nowe_symptomy.split(',')
        symptomy[nowa_choroba] = nowe_symptomy
        options = [{'label': choroba, 'value': choroba} for choroba in symptomy.keys()]
        return options, f"Dodano chorobę: {nowa_choroba} z symptomami: {nowe_symptomy}"
    else:
        return dash.no_update, dash.no_update


@app.callback(
    [Output('komunikat-output', 'children'), Output('download-csv', 'data')],
    [Input('pobierz-csv-button', 'n_clicks')],
    [State('choroba-dropdown', 'value')]
)
def pobierz_csv_callback(n_clicks, choroba):
    if n_clicks > 0 and choroba:
        data = pobierz_dane(symptomy[choroba])
        csv_data = data.to_csv(index=False)

        return f"Pobrano dane dla choroby: {choroba}", dict(content=csv_data, filename=f"{choroba}.csv")
    else:
        return dash.no_update, dash.no_update

@app.callback(
    [Output('wykres1', 'figure'), Output('wykres2', 'figure')],
    [Input('wygeneruj-wykresy-button', 'n_clicks')],
    [State('choroba-dropdown', 'value')]
)
def generuj_wykresy_callback(n_clicks, choroba):
    if n_clicks > 0 and choroba:
        data = pobierz_dane(symptomy[choroba])
        return generuj_wykresy(data)
    else:
        return dash.no_update, dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
