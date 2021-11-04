# Customer Personality Analysis problem
DataSet : https://www.kaggle.com/imakash3011/customer-personality-analysis

## Goal: Analysis of company's ideal customers

## Problem Statement

Customer Personality Analysis is a detailed analysis of a company’s ideal customers. It helps a business to better understand its customers and makes it easier for them to modify products according to the specific needs, behaviors and concerns of different types of customers.

Customer personality analysis helps a business to modify its product based on its target customers from different types of customer segments. For example, instead of spending money to market a new product to every customer in the company’s database, a company can analyze which customer segment is most likely to buy the product and then market the product only on that particular segment.

Content Attributes:

### People:

ID: Customer's unique identifier
Year_Birth: Customer's birth year
Education: Customer's education level
Marital_Status: Customer's marital status
Income: Customer's yearly household income
Kidhome: Number of children in customer's household
Teenhome: Number of teenagers in customer's household
Dt_Customer: Date of customer's enrollment with the company
Recency: Number of days since customer's last purchase
Complain: 1 if customer complained in the last 2 years, 0 otherwise


### Products:

MntWines: Amount spent on wine in last 2 years
MntFruits: Amount spent on fruits in last 2 years
MntMeatProducts: Amount spent on meat in last 2 years
MntFishProducts: Amount spent on fish in last 2 years
MntSweetProducts: Amount spent on sweets in last 2 years
MntGoldProds: Amount spent on gold in last 2 years


### Promotion:

NumDealsPurchases: Number of purchases made with a discount
AcceptedCmp1: 1 if customer accepted the offer in the 1st campaign, 0 otherwise
AcceptedCmp2: 1 if customer accepted the offer in the 2nd campaign, 0 otherwise
AcceptedCmp3: 1 if customer accepted the offer in the 3rd campaign, 0 otherwise
AcceptedCmp4: 1 if customer accepted the offer in the 4th campaign, 0 otherwise
AcceptedCmp5: 1 if customer accepted the offer in the 5th campaign, 0 otherwise
Response: 1 if customer accepted the offer in the last campaign, 0 otherwise


### Place:

NumWebPurchases: Number of purchases made through the company’s web site
NumCatalogPurchases: Number of purchases made using a catalogue
NumStorePurchases: Number of purchases made directly in stores
NumWebVisitsMonth: Number of visits to company’s web site in the last month


## Target
Need to perform clustering to summarize customer segments. (Unsupervised learning and no need to split dataset into train and test)

## Instructions:

Please download the whole project. Here the problem is a clustering (unsupervised learning) model so we are not going to have a train, test and validation dataframe. First you need to run the "train.py" file to train the model, Then run the "predict.py" file to see the reuslt you need to run the code which is saved in "result_on_localhost.py" by executing it the result will show up as a plot.

## Model deployment as a web service on local machine
For actual use of a model in real world, it needs to be deployed as a service (application) so that users (e.g. in this case Bank's staff who are supposed to call customer for Term Deposit subscription, can use this service. They can now send customer data to the service and get a prediction whether the customer is likely to make a Term deposit or not and hence whether it would be benificial to make the call to customer).

To test the model deployment as a web service - open 2 separate terminal sessions into your machine (where all this code resides) and activate the virtual environment as explained in 4. Virtual environment and package dependencies

From one terminal session run the following command to host the prediction model as a web service.

waitress-serve --listen 0.0.0.0:9696 predict.py
From other terminal session from the cloned project directory, execute the following command to make a request to this web service

python predict.py

## Deploy model as a web service to Docker container
You can deploy the trained model as a web service running inside a docker container on your local machine.

Pre-requisites: You should have Docker installed and running on the machine where you want to perform model deployment to docker. Run the below commands to check whether docker service is running and then to see if any docker containers are running.

systemctl status docker
docker ps -a
Following are the steps to do this:

Clone this repo (if you have not done this already. If done then skip this step)
Change to the directory that has the model file, python script (predict.py) for the web service and other required files
cd mlzoomcamp-midterm-project/app-deploy
Build docker image named Customer_Personality_Analysis
docker build -t "Customer_Personality_Analysis" .
Check docker image available. Output of below command should show the image with name Customer_Personality_Analysis
docker images
Create a docker container from the image. The model prediction script as a web service will then be running inside this container.
Below command will create and run a docker container named Customer_Personality (--name Customer_Personality) running as a daemon i.e.
non-interactive mode (-d), mapping the port 9696 on host to port 9696 on container (-p 9696:9696 first port is host port, second is container port. 
If you want to map different port on host just change the first number), from image bank-td-prediction. The container will be deleted if stopped or when you shutdown your machine (--rm).

docker run --rm --name Customer_Personality -d -p 9696:9696 Customer_Personality_Analysis

Check whether docker container running. Below command should show the container in Running state and not Exited.

docker ps -a

Test sending some sample customer data to the web service and see the results. For this you can use the request.py script provided as part of this repo, 
which has some sample customer entries and can make a request to the Web app service. Ensure you have activated the virtual environment as explained in 4.
Virtual environment and package dependencies. Check whether you are already in the project directory which you cloned from git. If not change to that directory.

python predict.py

