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
    
    if pr_once == 'yes':
        speech_output = 'Hey {} '.format(user_name) + 'your total premium amount is {} '.format(prem_amt) + 'Which is due before {} '.format(due_date.strftime("%d")) + 'of {} '.format(due_date.strftime("%B")) + 'in {} '.format(due_date.strftime("%Y")) 
    else :
        due_date = start_date + relativedelta((today_date - start_date).days/365)
        speech_output = 'Hey {} '.format(user_name) + 'your total premium amount is {} '.format(prem_amt) +  "and you have paid {}".format(npr_paid) + 'premiums till now! And, your next due date is on {} '.format(due_date.strftime("%d")) + 'of {} '.format(due_date.strftime("%B")) + 'in {} '.format(due_date.strftime("%Y")) 
            
    return print(speech_output)        
           
           
        
def premium_alert(intent):
    prem_count, prem_amt, user_name, pr_once, npr_paid, start_date = premium(intent1)
    start_date = pd.Timestamp(start_date)
    today_date = datetime.datetime.now()
    prem_to_paid = (today_date - start_date).days/365   
    default_n = int(prem_to_paid) - npr_paid
    
    if default_n >= 2:
        
        speech_output = 'Hey {} '.format(user_name) + 'It seems that you have missed your last few premiums! please pay it before {}'.format(due_date.strftime("%d")) + 'of {} '.format(due_date.strftime("%B")) + 'in {} '.format(due_date.strftime("%Y"))  
    else :
        speech_output = 'Hey {} '.format(user_name) +'No premium due'
    return print(speech_output)

    # should_end_session = False
    # return build_response(session_attributes, build_speechlet_response(
    #     card_title, speech_output, reprompt_text, should_end_session))  
    
"""......................................................................................"""



# #Indentify user and add user function giving all the variables(This can be converted as intent handlers adter finalising the way to add user scenarios)
# def check_user (user_id):
    
#     user_df = pd.read_csv("D:/Work/Alexa/voicebot/user.csv")
#     row = user_df.loc[user_df.id == int(user_id),'name']
    
#     if len(row) != 0:
        
#         print("Hello " + row[0] + "! How can I help you today?")
        
#     else :
        
#         print("We do not have any record of you in our database! Would you like to register for our services?")
        

# """After Conforming if User wants us to add him in our Database, Alexa should be asking Following Questions:
    
#     'Can I please know your Name?' - name
#     'Can you tell me your age?' - age
#     'Please let me know your gender' - gender
#     'Are you married?' - married
#     'How many Children do you have'
#     'What is your BMI?'
#     'Do you smoke?'
    
#     Answer of these along with Customer id generated randomly can be appended in the existing database"""
        
# def add_user(name,age,gender,married,children,bmi,smoker):
    
#     user_df = pd.read_csv("D:/Work/Alexa/voicebot/user.csv")
    
#     user_id = np.random.randint(1000,10000)
#     new_user = [int(user_id),str(name),int(age),str(gender),str(married),int(children),float(bmi),str(smoker)]
    
#     user_df.loc[len(user_df)] = new_user
    
#     return user_df
    
    
    
          
