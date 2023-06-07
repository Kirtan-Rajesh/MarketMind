import dash_html_components as html
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
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
            className="flex",
            children=[
                html.Div(
                    className="h-screen w-1/3 backdrop-blur-10 bg-gradient-to-br from-black to-gray-800 rounded-lg shadow-md border border-gray-500",
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
                                    id="StockCode"
                                ),
                                html.Label("Enter Stock Code", className="form__label"),
                            ],
                        ),
                        html.Button("Stock Price", className="button4"),

                        html.Button("Indicators", className="button4 indicator2"),

                        html.Button(
                                children=[
                                html.Span("Stock Price"),
                                html.I()
                        ],
                            className="button3",
                            style={"--clr": "#FB2576"},
                        ),
                        
                        html.Button(
                                children=[
                                html.Span("Indicators"),
                                html.I()
                        ],
                            className="indicator button3",
                            style={"--clr": "#FB2576"},
                    )
                    ],
                ),
                html.Div(
                    className="flex",
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
                                                                html.Span("!", className="exclaimation",style={"margin-left": "6vw"}),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="aboutinfo2",
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
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)