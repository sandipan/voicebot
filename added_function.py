import pandas as pd
import numpy as np
import random

user_df = pd.read_csv("D:/Work/Alexa/voicebot/user.csv")
disease_df = pd.read_csv("D:/Work/Alexa/voicebot/disease.csv")
userclaim_df = pd.read_csv("D:/Work/Alexa/voicebot/userclaim.csv")
userprod_df = pd.read_csv("D:/Work/Alexa/voicebot/userprod.csv")
prod_df = pd.read_csv("D:/Work/Alexa/voicebot/prod.csv")
prodcov_df = pd.read_csv("D:/Work/Alexa/voicebot/prodcov.csv")


intent1 = {"slot" :{
          "premium": {
              "user_id" :2222,
              "prod_id" :1234 
              }
        }
    }

def ask_premium(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    # print("SESSION BELOW")
    # print(session)
    # session_attributes = {}
    # card_title = "Identify"
    user_df = pd.read_csv("D:/Work/Alexa/voicebot/user.csv")
    userprod_df = pd.read_csv("D:/Work/Alexa/voicebot/userprod.csv")
    prod_df = pd.read_csv("D:/Work/Alexa/voicebot/prod.csv")
    
    uid = intent['slot']['premium']['user_id']
    pid = intent['slot']['premium']['prod_id']
    
    prem_count = userprod_df.loc[(userprod_df.uid == int(uid)) & (userprod_df.pid == int(pid)),'nprpaid'].values[0]
    prem_amt = prod_df.loc[prod_df.id == int(pid), 'pramt']
     
    user_name = user_df.loc[user_df.id == int(uid), 'name']                           
    

    speech_output = 'Hey {} '.format(user_name.values[0]) + 'your total premium amount is {}'.format(prem_amt.values[0]) + " and you have paid {}".format(prem_count) + " premiums till now"
    
    return print(speech_output)
      # should_end_session = False
    # return build_response(session_attributes, build_speechlet_response(
    #     card_title, speech_output, reprompt_text, should_end_session))   
