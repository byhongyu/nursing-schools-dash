# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
from os import path
import zipcode


df = pd.read_csv('school.csv')



def generate_table(dataframe, max_rows = 10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe),max_rows))]
    )



app = dash.Dash()

app.layout = html.Div(children=[
    html.H4(children='Nursing Schools in California'),
    dcc.Slider(
        id='miles-slider',
        min=df['Distance from Pasadena (Miles)'].min(),
        max=df['Distance from Pasadena (Miles)'].max(),
        value=df['Distance from Pasadena (Miles)'].max()/2.0,
        step= 50.0,
        # marks={str(dis): str(dis) for dis in df['Distance from Pasadena (Miles)'].unique()}
    ),
    html.Div(id='table-div')
    ])

def get_lat_lon_from_zipcode(zipcode):
    zip = zipcode.isequal(zipcode)
    lat = zip.lat
    lon = zip.lon
    return (lat,lon)

@app.callback(
    Output('table-div','children'),
    [Input('miles-slider', 'value')])
def update_table(distance):
    dataframe = df[df['Distance from Pasadena (Miles)'] <= distance]
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), 100))]
    )
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
if __name__ == '__main__':
    app.run_server(debug=True)

