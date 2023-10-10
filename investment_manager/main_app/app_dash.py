from dash import Dash, html, dcc, Output, Input,dash_table
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.express as px
import datetime
from django_plotly_dash import DjangoDash
import ast
import plotly.graph_objects as go
from .app_engine import Portfolio
from .montecarlo_plotly import Graphs
import dash_daq as daq
import yfinance as yf
from dash.exceptions import PreventUpdate
import dash

portfolio = Portfolio()
graph = Graphs()

# Create a DjangoDash app instance
external_stylesheets = [dbc.themes.CERULEAN]
app = DjangoDash("AssetView", external_stylesheets=external_stylesheets)

# Define the path to the assetnames.txt file
file_path = "/Users/mac/Portfolio_Builder/env/investment_manager/main_app/assetnames.txt"

# Initialize the list of assets
stocks_list = []

# Read the list of assets from the file
try:
    with open(file_path, 'r') as file:
        file_contents = file.read()
        stocks_list = ast.literal_eval(file_contents)
except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")

# Define the layout of the Dash app
app.layout = html.Div(
    className="container-fluid",
    children=[
        html.Div(className="row justify-content-center", children=[
            html.P("Pick stocks that you are interested in (graph shows last stock you picked)[💡 for quick result turn switch OFF when picking assets]",
                   style={"font-family":"Helvetica"}),
            
            dcc.Dropdown(
                id="asset-name",
                options=[{"label": x, "value": x} for x in stocks_list],
                value=['AAPL', 'MSFT', 'GOOGL'],
                clearable=True,
                multi=True
            ),
            html.P(),

            dbc.Col(children=[
                html.P("Choose time frame for data visualizing live prices", 
                        style={'font-family':"Helvetica"}),
                dcc.RadioItems(
                id="time-interval",
                options=[
                    {'label': 'Daily', 'value': '1d'},
                    {'label': 'Monthly', 'value': '1mo'},
                    {'label': 'Yearly', 'value': '1y'},
                ],
                value="1y",
                inline = True,
                labelStyle={'display': 'inline-block', 'margin-right':'20px'}
            ),
            ]),
        
           
             dbc.Row([
                dbc.Col( dcc.Graph(id="stock-graph", figure={}), width=12),],
                style={"margin-left":"30px"}
                ),
            dbc.Row([ 
                html.Hr(),
                dbc.Col( children=[html.P("Turn switch on to create a portfolio and assess risk", 
                               style={"font-family":"Helvetica"}
                               ),       
                        html.P("[💡 for quick result turn switch OFF when picking assets]", 
                        style={"font-family":"Helvetica"}
                        )], 
                        width=6),



                dbc.Col(daq.BooleanSwitch(
                    id ="switch",
                    on = True,
                    color="#9B51E0",
                ), width=6),
                html.Hr(),

                
                ]),

            dbc.Row([
            dbc.Col( dcc.Graph(id="stock-piechart", figure={}), width=5),
            dbc.Col(dcc.Graph(id="risk-histogram", figure={}), width=7),
            ],
            style={"margin-left":"30px"}
            ),
            html.Hr(),

            dbc.Row([
                dbc.Col(

            dash_table.DataTable(
                id="allocation-table",
                columns=[
                    {"name": "Stock", "id": "stock"},
                    {"name": "Market Price", "id": "market_price"},
                    {"name": "Weight", "id": "weight"},
                    {"name": "Allocation ($100,000)", "id": "allocation"},
                    {"name": "Left Over", "id": "left_over"},
                ],
                data=[]
            )
                )
            ]),

                

        ])
    ]
)

# Define the callback to update the stock graph
@app.callback(
    Output("stock-graph", "figure"),
    Input("asset-name", "value"), 
    Input("time-interval", "value"),  
)

def update_stock_graph(selected_stock, time_interval):

    print('inside function')
    if not selected_stock:
        return {}  # No stock selected, return an empty figure
    
    #this section runs the efficient frontier

    if time_interval == "1d":
        interval = "5m"
    elif time_interval == "1mo":
        interval = "1h"
    else:
        interval = "1d"
    
    # Assuming you want to create traces for all selected stocks

    print("selected:", selected_stock)
    print("selected:", selected_stock[-1])

    df =yf.download(selected_stock[-1], period=time_interval, interval=interval)

    print("data frame from dash:","\n", df.head())

    trace = go.Scatter(
        x =df.index,
        y = df['Close'],
        fill = 'tozeroy',
        mode='lines',
        name=selected_stock[-1],
        marker = dict(color = df, colorscale ='Viridis'),

    )
    layout = go.Layout(
        title= 'stock data',
        xaxis=dict(title = 'Time', showgrid = False),
        yaxis=dict(title = selected_stock[-1], showgrid = False),
        plot_bgcolor='#fff',  # Set the background color of the plotting area
        # paper_bgcolor='#f2f2f2',
       
    )
    fig0 =go.Figure(data=[trace], layout=layout)
    return fig0
    

@app.callback(
    Output("stock-piechart", "figure"),
    Input("asset-name", "value"), 
    Input("switch","on"),
)
def update_piechart(selected_stock,on):

    if on:
        print(on)
        print('start_portfolio')
        portfolio.selected_assets(selected_stock)
        portfolio.run_montecarlo()
        weights = portfolio.cleaned_weights
        portfolio_returns = portfolio.portfolio_returns
        graph.create_graphs(weights, portfolio_returns=portfolio_returns)
        plot_div1 = graph.plot_div1


    return plot_div1


@app.callback(
    Output("risk-histogram", "figure"),
    Input("asset-name", "value"), 
    Input("switch","on"),
)
def update_histogram(selected_stock,on):

    if on:
        print(on)
        print('start_portfolio')
        portfolio.selected_assets(selected_stock)
        portfolio.run_montecarlo()
        weights = portfolio.cleaned_weights
        portfolio_returns = portfolio.portfolio_returns
        graph.create_graphs(weights,portfolio_returns=portfolio_returns)
        plot_div2 = graph.plot_div2



    return plot_div2


import yfinance as yf
import dash_table

@app.callback(
    Output("allocation-table", "data"),
    Input("asset-name", "value"), 
    Input("switch", "on"),
)
def update_table(selected_stock, on):
    print('TABLE FUNC IS IN')

    if on:
        print(on)
        print('START TABLE')
        portfolio.selected_assets(selected_stock)
        weights = portfolio.cleaned_weights

        table_data = []
        leftover = 100000
        for stock, weight in weights.items():
            try:
                print('LET\'S TRY TOGETHER')
                stock = stock
                ticker = yf.Ticker(stock)
                data = ticker.history(period="1d")
                market_price = data['Close'].iloc[-1]  # Use the most recent closing price
                weight_percentage = weight * 100
                allocation = 100000 * weight
                leftover = leftover - allocation
                print('LEFTOVER MIGHT HAVE ISSUES')

                table_data.append({
                    "stock": stock,
                    'market_price': market_price,
                    "weight": weight_percentage,
                    "allocation": allocation,
                    "left_over": leftover,
                })

            except Exception as e:
                print('Error:', e)
                continue

        return table_data
    else:
        print("on was not picked")
        return dash.no_update  # Return dash.no_update when 'on' is False to prevent updating the table

        









