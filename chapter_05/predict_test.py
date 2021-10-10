
import requests

url = 'http://localhost:9696/predict'

customer = {
    "gender": "female",
    "seniorcitizen": 0,
    "partner": "yes",
    "dependents": "no",
    "phoneservice": "no",
    "multiplelines": "no_phone_service",
    "internetservice": "dsl",
    "onlinesecurity": "no",
    "onlinebackup": "yes",
    "deviceprotection": "no",
    "techsupport": "no",
    "streamingtv": "no",
    "streamingmovies": "no",
    "contract": "month-to-month",
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check",
    "tenure": 24,
    "monthlycharges": 29.85,
    "totalcharges": (24 * 29.85)
}
customer_id = 'msmoh@gmail.com'

response = requests.post(url, json = customer).json()
print(response)

if response['churn'] == True:
    print("sending promo to email %s" % customer_id)
else:
    print('do not send the email')