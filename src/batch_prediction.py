from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import date, timedelta
import pandas as pd
import numpy as np
import pickle

with open('./models/anomaly_model.pkl', 'rb')as file:
    anomaly_model = pickle.load(file)

today = date.today() - timedelta(1)
#today = date.today()

#Google Big Query Credentials
gbq_table = "Dataset.mbb"
gcp_project_id = "tsf-project-344410"
gbq_destination = f'{gcp_project_id}.{gbq_table}'
credentials = service_account.Credentials.from_service_account_file("./config/GCP_TSF_ServiceAccount.json")
bigquery_client = bigquery.Client(credentials = credentials)
table_ref = bigquery_client.dataset('Dataset').table('anomaly_isolation')
table = bigquery_client.get_table(table_ref)

# Create the dataframe based on gbq by using SQL Query.
mbb_query = """
SELECT *
FROM `tsf-project-344410.Dataset.mbb`
ORDER BY Date DESC
LIMIT 1
"""

mbb_2days_query = """
SELECT *
FROM `tsf-project-344410.Dataset.mbb`
ORDER BY Date DESC
LIMIT 2
"""

mbb = (
     bigquery_client.query(mbb_query)
     .result()
     .to_dataframe(create_bqstorage_client = True,))

mbb_2days = (
     bigquery_client.query(mbb_2days_query)
     .result()
     .to_dataframe(create_bqstorage_client = True,))

'''0. Downcasting the dataset'''
#cols = list(mbb.columns)
#type_list = list(mbb.dtypes.values)
#for i, t in enumerate(type_list):
#        if 'int' in str(t):
#            if (mbb[cols[i]].min() > np.iinfo(np.int8).min) and (mbb[cols[i]].max() < np.iinfo(np.int8).max):
#                mbb[cols[i]] = mbb[cols[i]].astype(np.int8)
#                
#            elif (mbb[cols[i]].min() > np.iinfo(np.int16).min) and (mbb[cols[i]].max() < np.iinfo(np.int16).max):
#                mbb[cols[i]] = mbb[cols[i]].astype(np.int16)
#                
#            elif (mbb[cols[i]].min() > np.iinfo(np.int32).min) and (mbb[cols[i]].max() < np.iinfo(np.int32).max):
#                mbb[cols[i]] = mbb[cols[i]].astype(np.int32)
#            
#            else:
#                mbb[cols[i]] = mbb[cols[i]].asypes(np.int64)
#        elif 'float' in str(t):
#            if (mbb[cols[i]].min() > np.finfo(np.float16).min) and (mbb[cols[i]].max() < np.finfo(np.float16).max):
#                mbb[cols[i]] = mbb[cols[i]].astype(np.float16)
#                
#            elif (mbb[cols[i]].min() > np.finfo(np.float32).min) and (mbb[cols[i]].max() < np.finfo(np.float32).max):
#                mbb[cols[i]] = mbb[cols[i]].astype(np.float32)
#            
#            else:
#                mbb[cols[i]] = mbb[cols[i]].asypes(np.float64)
#
mbb['Volume'] = mbb['Volume'].astype(np.int32)

'''1. Data Preprocessing
    * preprocess the input feature from gbq
'''
df = mbb.copy()
df = df[['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']]
df.reset_index(drop=True, inplace=True)


'''2. Batch Prediction for Anomaly Detection'''
pred = pd.Series(anomaly_model.predict(df.values))
df = df.merge(pred.rename('Anomaly_Flag'), left_index = True, right_index = True)


'''3. Data Enrichment
    * Added Date, Yesterday_Change & Percentage_Change columns
'''
date_column = mbb['Date'].reset_index(drop = True)
df = df.merge(date_column.rename('Date'), left_index = True, right_index = True)
df = df[['Date','Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Anomaly_Flag']]

#df['Yesterday_Close'] = 0.2
#df['Percentage_Change'] = 0.2
#for i in range(0,2):  
#    df['Yesterday_Close'][i] = mbb_2days.iloc[i+1]['Close']

df['Yesterday_Close'] = mbb_2days.iloc[1]['Close']
df['Percentage_Change']= ((df['Close'] - df['Yesterday_Close']) / df['Close']) * 100
df['Percentage_Change'] = np.round(df['Percentage_Change'],2)
df = df.replace(np.nan, 0)
df = df[['Date','Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Anomaly_Flag', 'Yesterday_Close', 'Percentage_Change']]

'''4. Insert the result into gbq'''
try:
    bigquery_client.insert_rows_from_dataframe(table = table, dataframe = df)
    print(f'The result inserted into Google Big Query for {today}')
except Exception as e:
    print(e)
    pass