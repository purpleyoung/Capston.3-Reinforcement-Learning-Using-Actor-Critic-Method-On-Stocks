import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from data_pipeline import preprocess_data
import matplotlib.pyplot as plt
from training_pipeline import backtest



tickers = ['AAPL','ACN','ADBE','ADI','ADP','ADSK','AKAM','AMAT','AMD','ANET','ANSS','APH','AVGO','BR','CDNS','CDW','CRM','CSCO','CTSH','CTXS','DXC','ENPH','FFIV','FIS','FISV','FLIR','FLT','FTNT','GLW','GPN','HPE','HPQ','IBM','INTC','INTU','IPGP','IT','JKHY','JNPR','KEYS','KLAC','LRCX','MA','MCHP','MPWR','MSFT','MSI','MU','MXIM','NLOK','NOW','NTAP','NVDA','NXPI','ORCL','PAYC','PAYX','PYPL','QCOM','QRVO','SNPS','STX','SWKS','TEL','TER','TRMB','TXN','TYL','V','VRSN','WDC','WU','XLNX','ZBRA']
periods = ['30day','7day']




app = dash.Dash(__name__, meta_tags = [{"name": "viewport", "content": "width=device-width"}])
application = app.server
# Dash application layout
app.layout = html.Div(children=[
    html.H1('myheading1'),
    html.Div([
        html.Div([
    		dcc.Dropdown(
    			id = "period",
    			multi = False,
    			searchable = True,
    			value = "",
    			placeholder = "Select Period",
    			options = [{"label": c, "value": c} for c in periods],
    			className = "dcc_compon"
                ),
            dcc.Dropdown(
    			id = "ticker",
    			multi = False,
    			searchable = True,
    			value = "",
    			placeholder = "Select ticker",
    			options = [{"label": c, "value": c} for c in tickers],
    			className = "dcc_compon"
                ),
            html.Div([
                html.Div(id='your_output_here', children=''),
                    ],      
                    className='eight columns'),
                ])
    ])
])


# Callbacks and functions
@app.callback(Output('your_output_here', 'children'),
              [Input('period', 'value'),
               Input('ticker', 'value')], methods=['GET', 'POST'])
def drop_down_results(period, ticker):
    """[Uses user input to return images of model performance metrics.
        This function could go in several directions. Ideally it should provide
        on the fly backtesting but for now it serves images generated by backtesting,
        which need to be refreshed manually at this point.]

    Args:
        period ([string]): [Indicates cutoff for model testing]
        ticker ([string]): [Ticker for a stock user wats to know about.]

    Returns:
        [png image file]: [Could be anything]
    """
    #env = backtest(ticker,period)
    # should return 'an' image based on stock and period chosen.
    image_you_chose = f'{period}-{ticker}.png'
    
    return html.Img(src=app.get_asset_url(image_you_chose), style={'width': 'auto', 'height': '50%'})


if __name__ == '__main__':
    application.run(debug=True, port=5000)
        