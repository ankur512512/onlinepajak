import boto3
from io import StringIO
import json
import time
import getopt, sys
from datetime import date, timedelta, datetime
from datadog import initialize, api
import os

# Initializing boto3 resource with required parameters from env variables
s3 = boto3.resource(
    service_name='s3',
    region_name='ap-southeast-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
)

# Initializing the api with required parameters env variables
initialize(
    api_key=os.getenv('DATADOG_API_KEY'),
)

today = []
yesterday = []

my_bucket=s3.Bucket('online-pajak-hr-ops-technical-exercice')
bucket_list_today = []
bucket_list_yesterday = []


## Setting date as per user input
try:
    if (str(sys.argv[2]) != ""):
        date_today = datetime.strptime(str(sys.argv[2]), '%Y-%m-%d').date()

        date_yesterday = date_today - timedelta(days = 1)
except:
        date_today = date.today()

        date_yesterday = date_today - timedelta(days = 1)

## Get Data from AWS Bucket function
def getData(date_today, date_yesterday):
    ## For today
    for file in my_bucket.objects.filter(Prefix = date_today):
        file_name=file.key
        if file_name.find(".json")!=-1:
            bucket_list_today.append(file.key)

    for file in bucket_list_today:
        obj = s3.Object('online-pajak-hr-ops-technical-exercice',file)
        data=obj.get()['Body'].read()
        data1=json.loads(data)
        today.append(data1['transaction_id'])

    ## For yesterday
    for file in my_bucket.objects.filter(Prefix = date_yesterday):
        file_name=file.key
        if file_name.find(".json")!=-1:
            bucket_list_yesterday.append(file.key)

    for file in bucket_list_yesterday:
        obj = s3.Object('online-pajak-hr-ops-technical-exercice',file)
        data=obj.get()['Body'].read()
        data1=json.loads(data)
        yesterday.append(data1['transaction_id'])
    

# New Transaction function
def fresh(li1, li2):
    return list(set(li1) - set(li2))

# Lost Transaction fucntion
def lost(li1, li2):
    return list(set(li2) - set(li1))

# Print metrics to standard output function
def stout(output1, output2):
    print(json.dumps(output1))
    print(json.dumps(output2))

# Main function
def mainfunct():
      getData(str(date_today), str(date_yesterday))
      new_transaction = fresh(today, yesterday)
      lost_transaction = lost(today, yesterday)
      count_new_trasaction=str(len(new_transaction))
      count_lost_transaction=str(len(lost_transaction))

      output1 ={
            "metric" : "business.a_process.transaction_new",
            "value" : count_new_trasaction,
            "timestamp" : int(time.time()) 
        }
      output2 ={
            "metric" : "business.a_process.transaction_lost",
            "value" : count_lost_transaction,
            "timestamp" : int(time.time()) 
        }
      try:
        if (str(sys.argv[1]) == "stdout"):
            stout(output1, output2)
        elif(str(sys.argv[1]) == "send"):
            metrics = [{'metric': 'business.a_process.transaction_new', 'value': count_new_trasaction, 'points': [int(time.time())], 'timestamp': int(time.time())},
           {'metric': 'business.a_process.transaction_lost', 'value': count_lost_transaction, 'points': [int(time.time())], 'timestamp': int(time.time())} 
          ]
            api_response=api.Metric.send(metric='mymetric', metrics=metrics)
            print(api_response)
      except:
            if(len(sys.argv)==1):
                print("Invalid or no parameter specified, Please pass any one argument as shown below:\npython.exe bucket.py send  #Send data to datadog; setting current date as today's date\npython.exe bucket.py send 2021-08-26  #Send data to datadog; setting current date as 2021-08-26\npython.exe bucket.py stdout  #Print metrics as stdout; setting current date as today's date\npython.exe bucket.py stdout 2021-08-26  #Print metrics as stdout; setting current date as 2021-08-26")
mainfunct()