# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 16:24:04 2021

@author: Akash Gupta
"""

import pandas as pd
import numpy as np
import random
import datetime
from dateutil.relativedelta import relativedelta



#Load all the data for checking functions
user_df = pd.read_csv("D:/Work/Alexa/voicebot/user.csv")
disease_df = pd.read_csv("D:/Work/Alexa/voicebot/disease.csv")
userclaim_df = pd.read_csv("D:/Work/Alexa/voicebot/userclaim.csv")
userprod_df = pd.read_csv("D:/Work/Alexa/voicebot/userprod.csv")
prod_df = pd.read_csv("D:/Work/Alexa/voicebot/prod.csv")
prodcov_df = pd.read_csv("D:/Work/Alexa/voicebot/prodcov.csv")


#create an intent in json format
intent1 = {"slot" :{
          "premium": {
              "user_id" :2222,
              "prod_id" :1234 
              }
        }
    }

intent2 = {"slot" :{
          "premium": {
              "user_id" :1111,
              "prod_id" :1234 
              }
        }
    }

intent3 = {"slot" :{
          "premium": {
              "user_id" :2222,
              "prod_id" :2345 
              }
        }
    }

intent4 = {"slot" :{
          "premium": {
              "user_id" :1111,
              "prod_id" :2345 
              }
        }
    }

def remove_user(intent):
    user_df = pd.read_csv("D:/Work/Alexa/voicebot/user.csv")
    
    uid = intent['slot']['premium']['user_id']
    i = user_df[user_df.id == uid].index
    
    user_df = user_df.drop(i)
    
    return user_df

#Premium helper function for both ask_premium and alert_premium   
def premium(intent):

    user_df = pd.read_csv("D:/Work/Alexa/voicebot/user.csv")
    userprod_df = pd.read_csv("D:/Work/Alexa/voicebot/userprod.csv")
    prod_df = pd.read_csv("D:/Work/Alexa/voicebot/prod.csv")
    userprod_df['date'] = pd.to_datetime(userprod_df['date'])
    
    uid = intent['slot']['premium']['user_id']
    pid = intent['slot']['premium']['prod_id']
    
    prem_count = userprod_df.loc[(userprod_df.uid == int(uid)) & (userprod_df.pid == int(pid)),'nprpaid'].values[0]
    prem_amt = prod_df.loc[prod_df.id == int(pid), 'pramt'].values[0]
    user_name = user_df.loc[user_df.id == int(uid), 'name'].values[0]                           
    pr_once = prod_df.loc[prod_df.id == int(pid), 'pronce'].values[0]
    start_date = userprod_df.loc[(userprod_df.uid == int(uid)) & (userprod_df.pid == int(pid)),'date'].values[0]
    npr_paid = userprod_df.loc[(userprod_df.uid == int(uid)) & (userprod_df.pid == int(pid)),'nprpaid'].values[0]
    # speech_output = 'Hey {} '.format(user_name.values[0]) + 'your total premium amount is {}'.format(prem_amt.values[0]) + " and you have paid {}".format(prem_count) + " premiums till now"
    
    return prem_count, prem_amt, user_name, pr_once, npr_paid, start_date


def ask_premium(intent):
    prem_count, prem_amt, user_name, pr_once, npr_paid, start_date = premium(intent)
    start_date = pd.Timestamp(start_date)
    due_date = start_date + relativedelta(years =1)
    today_date = datetime.datetime.now()
    real_paid = int((today_date - start_date).days/365)
    
    if pr_once == 'yes' and npr_paid == 0:
        speech_output = 'Hey {} '.format(user_name) + 'your total one time premium amount is {}! '.format(prem_amt) + 'Its not paid yet! Please Pay it ASAP'
    elif pr_once == 'yes' and npr_paid == 1 :
        speech_output = 'Hey {} '.format(user_name) + 'your total one time premium amount was {}! Payment is done.Thanks!.'.format(prem_amt)
        
    elif pr_once == 'no':   
        due_date = start_date + relativedelta(years = npr_paid)
        if npr_paid < real_paid:
            speech_output = 'Hey {} '.format(user_name) + 'your total premium amount is {} and you have missed your last {} yearly premiums! '.format(prem_amt, (real_paid - npr_paid)) + "Please pay it ASAP"
        elif npr_paid == real_paid:
            speech_output = 'Hey {} your total premium amount is {}! '.format(user_name,prem_amt)  +  "you must pay your next premium before {} ".format(due_date.strftime("%d")) + '{},'.format(due_date.strftime("%B")) + '{}'.format(due_date.strftime("%Y"))
    return print(speech_output)     
           
           
        
def premium_alert(intent):
    prem_count, prem_amt, user_name, pr_once, npr_paid, start_date = premium(intent)
    start_date = pd.Timestamp(start_date)
    today_date = datetime.datetime.now()
    prem_to_paid = int((today_date - start_date).days/365) 
    default_n = int(prem_to_paid) - npr_paid
    
    if pr_once == 'no':
        due_date = start_date + relativedelta(years = prem_to_paid)
        if default_n >= 2:
            speech_output = 'Hey {} '.format(user_name) + 'you missed your last few premiums! please pay it ASAP'  
        elif default_n ==1 :
            speech_output = 'Hey {} '.format(user_name) +'Your last premium was missed. Please pay your premium before {} '.format(due_date.strftime("%d")) + 'of {} '.format(due_date.strftime("%B")) + 'in {} '.format(due_date.strftime("%Y"))
        elif default_n ==0 :
            speech_output = 'Hey {} '.format(user_name) + 'No Premium alerts! Thanks for being our valuable Customer'
        
    elif pr_once =='yes' and npr_paid == 0:
        speech_output = 'Hey {} '.format(user_name) + 'your total premium amount is {} which is not yet paid!.'.format(prem_amt) + 'Please Pay it ASAP' 
    
    else :
        speech_output = 'No Alerts for premium'
    return print(speech_output)
