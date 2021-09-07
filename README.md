## Please install below modules first for this project to work

`pip3 install boto3 datadog`

## After that please export below environment variables as per your choice

`export AWS_ACCESS_KEY=<your-aws-access-key>`  
`export AWS_SECRET_KEY=<your-aws-secret-key>`  
`export DATADOG_API_KEY=<your-datadog-api-key>`

## Then clone this git repo and cd into it

`git clone https://github.com/ankur512512/onlinepajak.git`  
`cd onlinepajak`

## Then execute the script using any of the below options:

`python bucket.py send` # Send data to datadog; setting current date as today's date  
`python bucket.py send 2021-08-26` # Send data to datadog; setting current date as 2021-08-26  
`python bucket.py stdout` # Print metrics as stdout; setting current date as today's date  
`python bucket.py stdout 2021-08-26` # Print metrics as stdout; setting current date as 2021-08-26

