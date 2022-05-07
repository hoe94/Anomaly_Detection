from google.oauth2 import service_account
from google.cloud import bigquery
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import pickle
#import hydra
#from omegaconf import DictConfig

#Google Big Query Credentials
gbq_table = "Dataset.mbb"
gcp_project_id = "tsf-project-344410"
gbq_destination = f'{gcp_project_id}.{gbq_table}'
credentials = service_account.Credentials.from_service_account_file("./config/GCP_TSF_ServiceAccount.json")
bigquery_client = bigquery.Client(credentials = credentials)

# SQL Query.
query_string = """
SELECT *
FROM `tsf-project-344410.Dataset.mbb`
WHERE Date >= '2020-03-18'
ORDER BY Date ASC
"""

mbb = (
     bigquery_client.query(query_string)
     .result()
     .to_dataframe(create_bqstorage_client = True,))

#@hydra.main(config_path="../config", config_name="config")
#def isolation_forest_model(config: DictConfig):
#    contamination = config.base_model.contamination
#    mbb_len = mbb.shape[0]
#    anomaly_model = IsolationForest(n_estimators = 100, contamination = contamination, max_samples = mbb_len, max_features = 6) 
#    return anomaly_model

def data_preprocessing(df: pd.DataFrame, column_list: list):
    df = df[column_list]
    df.reset_index(drop=True, inplace=True)
    return df
   
def data_enrichment(df1: pd.DataFrame, df2: pd.DataFrame):
    date = df1['Date'].reset_index(drop = True)
    df = df2.merge(date.rename('Date'), left_index = True, right_index = True)
    df = df[['Date','Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Anomaly_Flag']]


    df['Yesterday_Close'] = df['Close'].shift(1)
    #df['percentage_change'] = ((df['Close'] - df['shift']) / df['Close']) * 100
    df['Percentage_Change'] = ((df['Close'] - df['Yesterday_Close']) / df['Close']) * 100
    df['Percentage_Change'] = np.round(df['Percentage_Change'],2)
    df = df.replace(np.nan, 0)

    df = df[['Date','Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Anomaly_Flag', 'Yesterday_Close', 'Percentage_Change']]
    return df

def main():
    column_list = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
    mbb_len = mbb.shape[0]
    anomaly_model = IsolationForest(n_estimators = 100, contamination = 0.10, max_samples = mbb_len, max_features = 6) 

    df = data_preprocessing(mbb, column_list)
    anomaly_model.fit(df.values)
    pred = pd.Series(anomaly_model.predict(df.values))
    df = df.merge(pred.rename('Anomaly_Flag'), left_index = True, right_index = True)
    df = data_enrichment(mbb, df)
    with open('./models/anomaly_model.pkl', 'wb')as file:
        pickle.dump(anomaly_model, file)
    df.to_csv('./data/results.csv', index = False)

if __name__ == "__main__":
    main()