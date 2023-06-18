from dash import html
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State, MATCH, ALL
from datetime import datetime as dt
import yfinance as yf
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go 
import requests

app = Dash(__name__,)

app.layout = html.Div(
    className="body  ",
    children=[
        html.Link(
            href="https://fonts.googleapis.com/css?family=Red+Hat+Display:900&display=swap",
            rel="stylesheet",
        ),
        html.Link(
            href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.15/dist/tailwind.min.css",
            rel="stylesheet",
        ),
        html.Link(
            rel="stylesheet",
            href="styles.css",
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Roboto:700",
            rel="stylesheet",
        ),
        html.Div(
            className="flex",
            children=[
                html.Div(
                    className="h-screen  sidepanel  backdrop-blur-10 bg-gradient-to-br from-black to-gray-800 shadow-md border border-gray-500",
                    children=[
                        html.Div(
                            className="lightlowerborder h-24 text-center border-b-4 flex items-center justify-center",
                            children=[
                                html.H1("MarketMind", className="font-bold font-red-hat-display font-sans text-white"),
                                html.Span(".", className="font-bold font-red-hat-display font-sans text-pink-500"),
                            ],
                        ),
                        html.Div(
                            className="form__group field",
                            children=[
                                dcc.Input(
                                    type="text",
                                    className="form__field",
                                    placeholder="Stock Code",
                                    name="name",
                                    id="StockCode",
                                    autoComplete='off'
                                ),
                                html.Label("Enter Stock Code", className="form__label"),
                            ],
                        ),
                        html.Br(),
                        
                        html.Button("Stock Price", className="button4",id="StockPrice2"),

                        html.Button("Indicators", className="button4 indicator2",id="Indicator2"),

                        html.Button(
                                children=[
                                html.Span("Stock Price"),
                                html.I()
                        ],
                            className="button3",id="StockPrice",
                            style={"--clr": "#FB2576"},
                        ),
                        
                        html.Button(
                                children=[
                                html.Span("Indicators "),
                                html.I()
                        ],
                            className="indicator button3",id="Indicator",
                            style={"--clr": "#FB2576"},
                    ),
                    dcc.DatePickerRange(id='my-date-picker-range',
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            calendar_orientation='horizontal',
                            className="dark-datepicker",
                            min_date_allowed=dt(1995, 8, 5),
                            max_date_allowed=dt.now(),
                            initial_visible_month=dt.now(),
                            end_date=dt.now().date()
                        ),
                        html.Div(
                            html.Button(
                                children=[
                                html.Span("Forecast"),
                                html.I()
                        ],
                            className="button3 forecast",id="Forecast",
                            style={"--clr": "#00FF00"},
                        ),
                        ),
                        html.Button("Forecast", className=" button4 forecast2",id="forecast2"),

                    ],

                ),

                html.Div(
                [
                html.Div(
                    [  # header
                        html.Img(id="stocklogo", className="headerimg"),
                        html.P(id="ticker", className="tickername")
                    ],
                    className="header"),
                html.Div(id="description", className="description"),
                html.Br(),
                html.Div(id="forecast-content",className="forecastlayout"),
                html.Br(),
                html.Div([], id="graphs-content",className="graphs"),
                html.Br(),
                html.Div([], id="main-content",className="graphs")
                ],
                className="content flex"),

                html.Div(
                    className="flex ",id="homepage",
                    children=[
                        html.Div(
                            children=[
                                html.H1("Master the Market with Precision:", className="font-black demo-2 text-white customheight"),
                            ],
                        ),
                        html.Div(
                            className="mainlogomedia",
                            children=[
                                html.Div(
                                    className="mainlogo hover:scale-110",
                                    children=[
                                        html.H1("Market"),
                                        html.H1("Mind."),
                                    ],
                                ),
                                html.H1("Your Data-Driven Investment Companion", className="font-black belowmm demo-2"),
                                html.Div(
                                    className="about",
                                    children=[
                                        html.Div(
                                            className="animated-title",
                                            children=[
                                                html.Div(
                                                    className="text-top",
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Span("About"),
                                                                html.Span("This"),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="text-bottom",
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div("Website"),
                                                                html.Span("!", className="exclaimation",style={"margin-left": "5.6rem"}),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="aboutinfo2 ",
                                            children=[
                                                html.P(
                                                    "Welcome to MarketMind, a cutting-edge single-page web application powered by Dash, a Python framework, and advanced machine learning models. "
                                                    "Our platform offers a comprehensive suite of features to help you make informed investment decisions. Explore company information, "
                                                    "also gaining access to dynamic stock plots tailored to the stock code you provide. Leveraging our powerful ML model, "
                                                    "MarketMind takes it a step further by providing predicted stock prices based on user-inputted dates. "
                                                    "Join us on this transformative journey, Helping you to navigate the world of stock markets with confidence and precision."
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),#homepage ends
                
            ],
        ),
    ],
)

# Store the current stock code
current_stock_code = None
df_more=pd.DataFrame()
@app.callback(
    [
        Output("description", "children"),
        Output("ticker", "children"),
        Output("homepage", "style"),
        Output("stocklogo", "src"),
        Output("graphs-content", "children"),
        Output("main-content", "children"),
        Output("forecast-content", "children")
    ],
    [Input('StockCode', 'n_submit')],
    [State('StockCode', 'value')]
)


def update_data(n, val):
    allow_duplicate=True
    global current_stock_code  # Declare current_stock_code as a global variable
    global DF
    if n:
        if val is None:
            raise PreventUpdate
        else:
            ticker = yf.Ticker(val)
            inf = ticker.info
            df = pd.DataFrame().from_dict(inf, orient="index").T
            


            logo_url = "https://logo.clearbit.com/" + '.'.join(ticker.info['website'].split('.')[1:])
            if current_stock_code != val:
                return (df['longBusinessSummary'].values[0],
                df['shortName'].values[0],
                {'display': 'none'},
                logo_url,None,None,None)
            current_stock_code = val  # Update the global variable with the new value
            return (
                df['longBusinessSummary'].values[0],
                df['shortName'].values[0],
                {'display': 'none'},
                logo_url,None,None,None
            )
    else:
        raise PreventUpdate


# callback for stocks graphs
@app.callback([
    Output("graphs-content", "children",allow_duplicate=True),
    Output("graphs-content","style",allow_duplicate=True)
], [
    Input("StockPrice", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("StockCode", "value")],
prevent_initial_call=True
)

def stock_price(n, start_date, end_date, val):

    if n == None:
        return [""]

    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(val, str(start_date), str(end_date))
        else:
            df = yf.download(val)

    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)],{ 'width':"70vw", 'margin-left': "2vw"}

def get_stock_price_fig(df):
    fig = px.line(df,
                  x="Date",
                  y=["Close", "Open"],
                  title="Closing and Opening Price vs Date")
    return fig


# callback for indicators
@app.callback([Output("main-content", "children",allow_duplicate=True),Output("main-content", "style",allow_duplicate=True)], [
    Input("Indicator", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("StockCode", "value")],prevent_initial_call=True)
def indicators(n, start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        return [""]

    if start_date == None:
        df_more = yf.download(val)
    else:
        df_more = yf.download(val, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)],{ 'width':'70vw', 'margin-left': '2vw'}


@app.callback([
    Output("graphs-content", "children",allow_duplicate=True),
], [
    Input("StockPrice2", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("StockCode", "value")],
prevent_initial_call=True
)

def stock_price(n, start_date, end_date, val):

    if n == None:
        return [""]

    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(val, str(start_date), str(end_date))
        else:
            df = yf.download(val)

    df.reset_index(inplace=True)

    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]

def get_stock_price_fig(df):
    fig = px.line(df,
                  x="Date",
                  y=["Close", "Open"],
                  title="Closing and Opening Price vs Date")
    return fig


# callback for indicator2
@app.callback([Output("main-content", "children",allow_duplicate=True)], [
    Input("Indicator2", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("StockCode", "value")],prevent_initial_call=True)
def indicators(n, start_date, end_date, val):
    global df_more
    if n == None:
        return [""]
    if val == None:
        return [""]

    if start_date == None:
        df_more = yf.download(val)
    else:
        df_more = yf.download(val, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)]



def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                     x="Date",
                     y="EWA_20",
                     title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines+markers')
    return fig

import joblib
from keras.models import load_model
scaler = joblib.load('scaler.gz')
regressor = load_model("model")
import numpy as np

@app.callback([
    Output("forecast-content", "children" ,allow_duplicate=True),
], [
    Input("Forecast", "n_clicks"),
], [State("StockCode", "value")],
prevent_initial_call=True
)
def predictionval(n,val):
    if n == None or val == None:
        return [""]
    else:
        df_more = yf.download(val,period="max")
        forecast_value=get_prediction(df_more)
    return [forecast_value]




def get_prediction(df):
    #ticker= yf.Ticker(val)
    #df = ticker.history(period="max")
    high_prices = df.loc[:,'High'].to_numpy()
    low_prices = df.loc[:,'Low'].to_numpy()
    data = (high_prices+low_prices)/2.0
    data = data.reshape(-1,1)
    data = scaler.transform(data).reshape(-1)
    X = []
    y = []
    for i in range(60, len(data)-60):
        X.append(data[i-60:i])
        y.append(data[i])
    X, y = np.array(X), np.array(y)
    predicted_stock_price = regressor.predict(X)
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
    output = f"The predicted value of the stock tomorrow: ${predicted_stock_price[-1, 0]}"
    return output

if __name__ == "__main__":
    app.run_server(debug=True)