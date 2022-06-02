# Anomaly Detection on Malaysia stock price in Covid-19 period

### Project Overview
Malaysia Government implement the national lockdown at 18th March 2020 due to the Covid-19 pandemic. The lockdown did a great job on prevent the pandemic getting worse. <br>
But at the same time, It brings the unexpectable damage to all the business in Malaysia. Maybank Sdn Bhd, Bellwether stock in Malaysia Bursa Stock Market. They can't escape this disaster too. <br>
The impact may reflect on the stock price. This may bring the risk to the management & investors. <br>
In this project, I built a ML Model to perform <strong>Anomaly Detection </strong> on Maybank stock price in Covid-19 period.(18th March 2020 - Now) <br>

- Project Objective
  * Dig out the unusual activity reflects on stock price
  * Investors can take into action to plan on investment profolio
  * Management can take note on unusual activitys on stock market
  
- Methodologies
  * Data Scrapping
  * Cloud technology
  * Machine Learning
  * Batch Anomaly Detection
  * Webapp Visualization

- Technologies Tools
  * Python
  * Pandas, Jupyter Notebook, VS Code
  * Isolation Forest, Scikit-Learn
  * Flask
  * HTML, CSS
  * Plotly
  * Google Cloud Platform (Google Cloud Storage, Google Cloud Function, Google Big Query, Google Cloud Scheduler)
  
- Project Architecture
  <img src = "https://github.com/hoe94/Anomaly_Detection/blob/main/Project_Architecture.png"></img>
  
### Data Scrapping
In the project phrase 1, I built the data scrapper to scrap maybank daily stock price in Yahoo Finance.<br>
It will ingest the data into Google Big Query for table reference. <br>
The scrapper are hosted at Google Cloud Function (GCF) and scheduled the function to run every day by Google Cloud Scheduler.<br>

### Batch Anomaly Detection
In the project phrase 2, I built the ML model by using <strong>Isolation Forest Algorithm </strong> to detect the anomaly from daily stock data.<br>
Isolation Forest Algorithm is a tree-based unsupervised algorithm. It splits data & features at the random threshold till all the points are isolated. <br>
We can tune the parameter, contamination to set the proportion of outliers in the dataset. In this project, we tuned the model to 10% of data are outliers among the data. <br>
It processes the scraped data from GBQ & the model will perform the batch anomaly detection on processed data.<br>
After this, the predicted data will ingest into GBQ for the visualization purpose.<br>
The model contains inside GCS. And the program hosted at Google Cloud Function (GCF) and scheduled the function to run every day by Google Cloud Scheduler.<br>

### Visualization
I have built a webapp dashboard to visualize the anomaly results by using Flask framework.<br>
User can observed that the red markers represents the anomaly/outlier in the line graph. <br>
Besides, user can check the closing price on the selected date in the below table. 
And the Percentage_Change% column describes the difference of stock price within 2 days in percentage%.
For example, Closing stock price for 28/4 is RM9.04, and the stock price is RM9.07.
Which means that it increase 0.33% on the stock price. <br>
I plan to host the webapp dashboard at the Heroku PAAS at the beginning. Due to the security issue, I have removed the webapp from heroku.

<img src = "https://github.com/hoe94/Anomaly_Detection/blob/main/front_end_screenshot.png"></img>
![Webapp Dashboard](https://github.com/hoe94/Anomaly_Detection/blob/main/Flask_Webapp_GIF.gif)

### Disclaimer:
This is the porfolio project for <strong>Education purpose</strong> only.
The content of this project is not intended as investment advice.
Please be responsible with your own investing decision.
Any action you take upon the information is at your own risk. <br>
<strong>The Author is not responsible for any trading losses.</strong>
