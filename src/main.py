from flask import Flask
#Google Big Query Library
from google.oauth2 import service_account
from google.cloud import bigquery
#Scikit Learn - Isolation Forest
from sklearn.ensemble import IsolationForest

#Google Big Query Credentials
gbq_table = "Dataset.mbb"
gcp_project_id = "tsf-project-344410"
gbq_destination = f'{gcp_project_id}.{gbq_table}'
credentials = service_account.Credentials.from_service_account_file("./GCP_TSF_ServiceAccount.json")
bigquery_client = bigquery.Client(credentials = credentials)

# SQL Query.
query_string = """
SELECT *
FROM `tsf-project-344410.Dataset.mbb` 
ORDER BY `Date` DESC
"""
df = (
     bigquery_client.query(query_string)
     .result()
     .to_dataframe(create_bqstorage_client = True,))

contamination = 0.15
mbb_len = df.shape[0]
anomaly_model = IsolationForest(n_estimators = 100, contamination = contamination, max_samples = mbb_len, max_features = 6)   

#app = Flask(__name__)

#@app.route('/')
#def Home():
#    dataframe = (
#    bigquery_client.query(query_string)
#    .result()
#    .to_dataframe(create_bqstorage_client = True,)
#)
#    print(dataframe.head())

#if __name__ == "__main__":
#    #app.run(debug = True)
#    Home()