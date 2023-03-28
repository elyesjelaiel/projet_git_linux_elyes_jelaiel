
import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from dash import dcc,html



import pandas as pd

import plotly.express as px

import requests
import datetime as dt



# Récupérer les données de Solana à partir de l'API de Coingecko

df = pd.read_csv("solana_price.txt",sep="\t",header=None, names=["solana"])
date = pd.read_csv("date.txt",sep="\t",header=None, names=["date"])


# Transformer les données en un DataFrame Pandas
date["date"] = pd.to_datetime(date["date"])

# Initialiser l'application Dash

app = dash.Dash(__name__)


# Définir la mise en page de l'application Dash

app.layout = html.Div(children=[

html.H1(children='Dashboard Solana'),


html.Div(children='''

 Graphique de prix de Solana (en USD) sur les 30 derniers jours :

    '''),
dcc.Graph(

id='solana-graph',

figure=px.line(df, x=date["date"], y=df["solana"], title='Prix de Solana (en USD)')

),


html.Div(children='''
 Tableau des prix de Solana (en USD) sur les 30 derniers jours :

    '''),
dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),

html.Div(children=[
html.H2('Daily Metrics'),
html.Div(id='daily-metrics')

])

])
def calculate_daily_metrics():
df["solana"]=df["solana"].apply(lambda x: x[1:])
df["solana"]=df["solana"].astype(float)
daily_volatility = round(df['solana'].std()*100,2)
today = df.iloc[-1]["solana"]
yesterday=df.iloc[-2]["solana"]
return daily_volatility, today, yesterday


@app.callback(Output('solana-graph','figure'),[Input('interval-component','n_intervals')]) 
def update_price_graph(n):
fig = go.Figure(data=go.Scatter(x=date["date"], y=df["solana"]))
return fig


@app.callback(Output('daily-metrics','children'),[Input('interval-component', 'n_intervals')]) 
def update_metrics(n):
daily_volatility, today, yesterday= calculate_daily_metrics()
text = html.Div([
html.P('Daily Volatility (annualized): {:.2%}'.format(daily_volatility)),
html.P('Price Today:{:.2f}'.format(today)),
html.P('Price Yesterday: {:.2f}'.format(yesterday))
])
return text


if __name__ == '__main__':
app.run_server(debug=True,host="0.0.0.0",port=8050)
