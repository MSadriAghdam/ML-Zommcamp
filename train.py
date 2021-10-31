#!/usr/bin/env python
# coding: utf-8

import pickle

from datetime import datetime as dt
import datetime
import re
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# parameters
C = 1.0
n_splits = 5
output_file = f'model_C={C}.bin'

# Data preparation
df =pd.read_csv("marketing_campaign.csv", sep="\t")

df.columns = df.columns.str.lower()
# handling thee missing values
df = df.fillna(df.income.mean())

# dimensionality reduction
df.education = df.education.replace(['PhD','Graduation', 'Master'], 'fully_Graduated')

df.education = df.education.replace(['Basic', '2n Cycle'], 'under_Graduated')

df.marital_status = df.marital_status.replace(['Married','Together'], 'Partner')

df.marital_status = df.marital_status.replace(['Single','Divorced', 'Widow', 'Alone','Absurd', 'YOLO'], 'Single')

# Extracting the age of the customers
df['age'] = (pd.Timestamp('now').year) - df['year_birth'] 
# drop year_birth after getting the age
df = df.drop('year_birth', axis=1)

# for how long a customer has been enrolled using Dt_Customer
def enrolment_period(dts):
    today = datetime.date.today()
    en_date = pd.to_datetime(dts).date() 
    days = today - en_date
    days = re.sub(" days, 0:00:00", "", str(days))
    days = int(days)
    return days

# Appling the function on dataframe
df['enrolment_days'] = df.dt_customer.apply(enrolment_period)

# Removing the outliers from the dataframe
df = df[df['income']< 200000]

# Regrouping expences:
df['expences'] = df[['mntmeatproducts' ,'mntfishproducts', 'mntsweetproducts',
                'mntwines', 'mntfruits','mntgoldprods' ]].sum(axis=1)
# Dropping the recent columns
drop_list = ['id', 'dt_customer', 'mntwines', 'mntfruits',
       'mntmeatproducts', 'mntfishproducts', 'mntsweetproducts','mntgoldprods' ]
df.drop(drop_list, axis = 1,inplace = True)

# Regrouping the responses to the campaines in a column: 
responces = ['acceptedcmp3', 'acceptedcmp4', 'acceptedcmp5', 'acceptedcmp1',
             'acceptedcmp2', 'response']


df['responces'] = df[responces].sum(axis = 1)

# if there is any responses it would be 1 otherwise it would be 0
def mapp(num):
    if num >=1:
        result = 1
    else:
        result = 0
    return result


df['responces'] = df['responces'].apply(mapp)
df.drop(responces, axis = 1,inplace = True)


# Regrouping the purchases
purchases = ['numdealspurchases', 'numwebpurchases',
       'numcatalogpurchases', 'numstorepurchases']

# Adding all the purchases in one column
df['purchases'] = df[purchases].sum(axis = 1) 
# Removing the other columns
df.drop(purchases, axis = 1,inplace = True)

# Combining the two columns kidhome and teenhome in one column
teen_kids = ['kidhome', 'teenhome']
# The number of children in teen_kids
df['teen_kids'] = df[teen_kids].sum(axis = 1)
# Dropping those columns 
df.drop(teen_kids, axis = 1,inplace = True)
# as these columns only have 1 value they can not affect our model we can drop these columns
df = df.drop(columns = ['z_costcontact','z_revenue' ], axis = 1)


# Replacing the age with the age groups

def age_category(age):
    if  25<=age <= 35:
        age = 0
    elif 35 < age <= 45:
        age = 1
    elif 45 < age <= 55:
        age = 2
    elif 55 < age <= 65:
        age = 3
    elif 65 < age <= 75:
        age = 4
    elif age > 75:  
        age = 5
    return age  

df.age = df.age.apply(age_category)

# One-Hot encoding
def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[feature_to_encode])
    res = pd.concat([original_dataframe, dummies], axis=1)
    res = res.drop(feature_to_encode, axis=1)
    return(res)

categorical =['education', 'marital_status']
df_encoded = encode_and_bind(df,categorical)


# Scaling
to_scale = ['income', 'recency', 'numwebvisitsmonth','enrolment_days', 'expences','purchases' ]
sc = StandardScaler()
X_scaled = sc.fit_transform(df_encoded[to_scale])

df_scaled = pd.DataFrame(X_scaled, columns=to_scale)
df_final = pd.concat([df_encoded.drop(to_scale, axis=1), df_scaled], axis=1)

df_final.dropna(inplace = True)

# Save the dataframe 
df_final.to_pickle("df_final.plk")
print('the dataframe is saved as a pickle file')

# K-means clustering
kmeans = KMeans(n_clusters=3, max_iter=2000, algorithm = 'auto')
model = kmeans.fit(df_final)

# Save the model
with open(output_file, 'wb') as f_out:
    pickle.dump(( model), f_out)

print(f'the model is saved to {output_file}')