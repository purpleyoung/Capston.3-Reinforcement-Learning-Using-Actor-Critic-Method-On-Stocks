import dash

app = dash.Dash(__name__)
application = app.server
.
. # your stuff ... 
.
if __name__ == '__main__':
    application.run(debug=True)