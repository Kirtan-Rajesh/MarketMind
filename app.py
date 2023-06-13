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
    className="body",
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
            className="flex sidepanel",
            children=[
                html.Div(
                    className="h-screen fixed  w-1/3 backdrop-blur-10 bg-gradient-to-br from-black to-gray-800 rounded-lg shadow-md border border-gray-500",
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
                            className="form__group field  Days",
                            children=[
                                dcc.Input(
                                    type="text",
                                    className="form__field  ",
                                    placeholder="Days",
                                    name="Days",
                                    id="Days",
                                    autoComplete='off'
                                ),
                                html.Label("Enter Number of Days", className="form__label"),
                            ],
                        )
                    ],

                ),

                html.Div(
                [
                html.Div(
                    [  # header
                        html.Img(id="stocklogo"),
                        html.P(id="ticker", className="tickername")
                    ],
                    className="header"),
                html.Div(id="description", className="decription_ticker"),
                html.Div([], id="graphs-content"),
                html.Div([], id="main-content"),
                html.Div([], id="forecast-content")
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


base_url = "https://api.benzinga.com/api/v1.1"
token = "be44938a8acf44a88803ce68825f0687" 

@app.callback(
    Output("stocklogo", "src"),
    [Input('StockCode', 'n_submit')],
    [State('StockCode', 'value')]
)
def update_data(n, val):
    if n:
        if val is None:
            raise PreventUpdate
        else:
            logo_url, _ = get_logo_url(val)  # Ignore the symbol by using "_"
            return logo_url
    else:
        raise PreventUpdate

def get_logo_url(stock_code):
    url = f"{base_url}/logos"
    headers = {"Accept": "application/json"}
    params = {"symbols": stock_code, "token": token}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        logos = response.json()
        if len(logos) > 0:
            logo_url = logos[0]["files"]["original"]
            return logo_url
    return None

@app.callback(
    [
        Output("description", "children"),
        Output("ticker", "children"),
        Output("homepage", "style")
    ],
    [Input('StockCode', 'n_submit')],
    [State('StockCode', 'value')]
)
def update_data(n, val):
    if n:
        if val is None:
            raise PreventUpdate
        else:
            ticker = yf.Ticker(val)
            inf = ticker.info
            df = pd.DataFrame().from_dict(inf, orient="index").T

            logo_url = get_logo_url(val)

            return (
                df['longBusinessSummary'].values[0],
                df['shortName'].values[0],
                {'display': 'none'}
            )
    else:
        raise PreventUpdate


# callback for stocks graphs
@app.callback([
    Output("graphs-content", "children"),
], [
    Input("StockPrice", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("StockCode", "value")])
def stock_price(n, start_date, end_date, val):
    if n == None:
        return [""]
        #raise PreventUpdate
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
                  title="Closing and Openning Price vs Date")

    return fig

# callback for indicators
@app.callback([Output("main-content", "children")], [
    Input("Indicator", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("StockCode", "value")])
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
    return [dcc.Graph(figure=fig)]


# callback for forecast
# @app.callback([Output("forecast-content", "children")],
#               [Input("forecast", "n_clicks")],
#               [State("n_days", "value"),
#                State("dropdown_tickers", "value")])
# def forecast(n, n_days, val):
#     if n == None:
#         return [""]
#     if val == None:
#         raise PreventUpdate
#     fig = prediction(val, int(n_days) + 1)
#     return [dcc.Graph(figure=fig)]




def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                     x="Date",
                     y="EWA_20",
                     title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines+markers')
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)