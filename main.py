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

df = (
    bigquery_client.query(query_string)
    .result()
    .to_dataframe(create_bqstorage_client = True,)
)

anomaly_df = df[df['Anomaly_Flag'] == -1]

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

axis = dict(
    showline=True,
    zeroline=False,
    showgrid=True,
    mirror=True,
    ticklen=4,
    gridcolor='#ffffff',
    tickfont=dict(size=10))
    
layout = dict(
    width=1000,
    height=865,
    autosize=False,
    title= 'Anomaly Detection for Maybank (1155) Stock Market price in Covid Era',
    margin=dict(t=75),
    showlegend=True,
    xaxis1=dict(axis, **dict(domain=[0, 1], anchor='y1', showticklabels=True)),
    yaxis1=dict(axis, **dict(domain=[2 * 0.21 + 0.20, 1], anchor='x1', hoverformat='.2f')))

fig = go.Figure(data=[Normal, Anomaly], layout = layout)
fig_JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


app = Flask(__name__, template_folder = './templates')
@app.route('/')
def index():
     return render_template('layout.html', fig1 = fig_JSON)

if __name__ == "__main__":
    app.run(debug = True)