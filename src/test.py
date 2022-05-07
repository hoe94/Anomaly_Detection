import json
from google.oauth2 import service_account
from google.cloud import bigquery
import plotly
import plotly.express as px

#Google Big Query Credentials
gbq_table = "Dataset.mbb"
gcp_project_id = "tsf-project-344410"
gbq_destination = f'{gcp_project_id}.{gbq_table}'
credentials = service_account.Credentials.from_service_account_file("./config/GCP_TSF_ServiceAccount.json")
bigquery_client = bigquery.Client(credentials = credentials)

query_string = """
SELECT *
FROM `tsf-project-344410.Dataset.mbb` 
WHERE Date >= '2020-03-18'
ORDER BY Date DESC
"""

df = (
    bigquery_client.query(query_string)
    .result()
    .to_dataframe(create_bqstorage_client = True,)
)

#fig = px.line(df, x = 'Date', y = 'Close', title = 'Maybank Stock Price Line Graph')
#fig_JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#print(json.loads(fig_JSON))
print(df.head())