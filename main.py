import json
from flask import Flask, send_file, render_template
from google.oauth2 import service_account
from google.cloud import bigquery

import plotly
import plotly.express as px
import plotly.graph_objs as go

#Google Big Query Credentials
gbq_table = "Dataset.mbb"
gcp_project_id = "tsf-project-344410"
gbq_destination = f'{gcp_project_id}.{gbq_table}'
credentials = service_account.Credentials.from_service_account_file("./config/GCP_TSF_ServiceAccount.json")
bigquery_client = bigquery.Client(credentials = credentials)

# SQL Query.
query_string = """
SELECT *
FROM `tsf-project-344410.Dataset.anomaly_isolation` 
WHERE Date >= '2020-03-18'
ORDER BY Date ASC
"""

graph_query_string = """
SELECT *
FROM `tsf-project-344410.Dataset.anomaly_isolation` 
WHERE Date >= '2020-03-18'
ORDER BY Date DESC
"""

df = (
    bigquery_client.query(query_string)
    .result()
    .to_dataframe(create_bqstorage_client = True,)
)

graph_df = (
    bigquery_client.query(graph_query_string)
    .result()
    .to_dataframe(create_bqstorage_client = True,)
)

anomaly_df = df[df['Anomaly_Flag'] == -1]
color_map = {1: ""'rgb(228, 222, 249)'"", -1: ""'rgb(247, 90, 90)'""}

#fig = px.line(df, x = 'Date', y = 'Close', markers = True, title = 'Anomaly Detection for Maybank (1155) Stock Market price in Covid Era')
#Plot the actuals points
Normal = go.Scatter(name = 'Normal',
                     x = df['Date'],
                     y = df['Close'],
                     xaxis='x1', yaxis='y1',
                     mode='lines',
                     marker=dict(size=12,
                                color="blue"))

#Highlight the anomaly points
Anomaly = go.Scatter(name="Anomaly",
                     showlegend=True,
                     x = anomaly_df['Date'],
                     y= anomaly_df['Close'],
                     mode='markers',
                     xaxis='x1',
                     yaxis='y1',
                     marker=dict(color="red",
                                size=11))

#Table which includes Date,Actuals,Change occured from previous point
table = go.Table(
    domain  =   dict(x = [0, 1], y = [0.1, 0.5]),
    columnwidth = [1, 2],
    # columnorder=[0, 1, 2,],
    header = dict(height = 20,
                values = [['<b>Date</b>'], ['<b>Closing Stock Price</b>'], ['<b>Percentage_Change%</b>']],
                line = dict(color = '#121212'),
                font = dict(color=['rgb(45, 45, 45)'], size=14),
                fill = dict(color='#797cf6')),

    cells = dict(values=[graph_df.round(3)[k].tolist() for k in ['Date', 'Close', 'Percentage_Change']],
                line = dict(color='#121212'),
                align = ['center'] * 5,
                font = dict(color = ['rgb(40, 40, 40)'] * 5, size = 12),
                suffix = [None] + [''] + [''] + ['%'] + [''],
                height = 27,
                fill = dict(color = [graph_df['Anomaly_Flag'].map(color_map)],#map based on anomaly level from dictionary
                )
                ))


axis = dict(
    showline=True,
    zeroline=False,
    showgrid=True,
    mirror=True,
    ticklen=4,
    gridcolor='#ffffff',
    tickfont=dict(size=20))
    
layout = dict(
    width=2100,
    height=600,
    autosize=False,
    title= 'Line Graph & Table about Maybank',
    margin=dict(t=75),
    showlegend=True,
    xaxis1=dict(axis, **dict(domain=[0, 1], anchor='y1', showticklabels=True)),
    yaxis1=dict(axis, **dict(domain=[2 * 0.21 + 0.20, 1], anchor='x1', hoverformat='.2f')))

fig = go.Figure(data=[Normal, Anomaly, table], layout = layout)
fig_JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


app = Flask(__name__, template_folder = './templates')
@app.route('/')
def index():
     return render_template('layout.html', fig1 = fig_JSON)

if __name__ == "__main__":
    app.run(debug = True)