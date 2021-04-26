import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime


import pandas_datareader.data as web


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
from mpld3 import plugins
np.random.seed(9615)

# Layout
app = dash.Dash()
app.title = "ML Sock Predict"
app.layout = html.Div(children=[
    html.H1('Stock Visualization Dashboard'),
    html.H4('Please enter the stock name'),
    dcc.Input(id="input", value='', type='text'),
    html.Div(id="output-graph")
])


# User Inputs
@app.callback(
    Output(component_id="output-graph", component_property='children'),
    [Input(component_id="input", component_property="value")]
)
def update_value(input_data):
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'yahoo', start, end)
    #return html(df)
    
    # generate df
    N = 100
    df = pd.DataFrame((.1 * (np.random.random((N, 5)) - .5)).cumsum(0),
                      columns=['a', 'b', 'c', 'd', 'e'],)
    
    # plot line + confidence interval
    fig, ax = plt.subplots()
    ax.grid(True, alpha=0.3)
    
    for key, val in df.iteritems():
        l, = ax.plot(val.index, val.values, label=key)
        ax.fill_between(val.index,
                        val.values * .5, val.values * 1.5,
                        color=l.get_color(), alpha=.4)
    
    # define interactive legend
    
    handles, labels = ax.get_legend_handles_labels() # return lines and labels
    interactive_legend = plugins.InteractiveLegendPlugin(zip(handles,
                                                             ax.collections),
                                                         labels,
                                                         alpha_unsel=0.5,
                                                         alpha_over=1.5, 
                                                         start_visible=True)
    plugins.connect(fig, interactive_legend)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Interactive legend', size=20)
    
    mpld3.show()
    return dcc.Graph(id="demo", figure={mpld3.show()})


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8000, debug=True)

    
    
