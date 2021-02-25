"""
AWS lambda code for Voicebot
### author: Sandipan Dey
"""

import random
import json

import pandas as pd

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_id_response(intent, session):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    print("SESSION BELOW")
    print(session)
    session_attributes = {}
    card_title = "Identify"
    df = pd.read_csv('user.csv')
    
    id = intent['slots']['id']['value']
    print(id)
    row = df.loc[df.id == int(id), 'name']
    
    if len(row) != 0:
        speech_output = 'Welcome {}'.format(row.values[0])
    else:
        speech_output = 'Your id is not there in my database!'
    reprompt_text = "I said " + speech_output
        
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_benefit_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Benefits"
    speech_output = 'what service do you want to know more about?'
    reprompt_text = "I said," + speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_service_response(intent, session):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    print("SESSION BELOW")
    print(session)
    session_attributes = {}
    card_title = "Service"
    #df = pd.read_csv('insurance.csv')
    #with open('test.json') as json_file:
    #    cov = json.load(json_file)['disease']
    cov = {'diabetes': {'prop': '100%', 'amt': '$20000', 'claimed': '$20'}, \
           'orthopedics': {'prop': '80%', 'amt': '$30000', 'claimed': '$4000'}}

    disease = intent['slots']['disease']['value']
    
    if disease in cov:  
        speech_output = 'your coverage for {} is {} and you have claimed {} of {}'.format(disease, cov[disease]['prop'], cov[disease]['claimed'], cov[disease]['amt'])
    else:
        speech_output = '{} is not covered in your policy'.format(disease)
    reprompt_text = "I said " + speech_output
        
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_recommend_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Recommendation"
    plans = ['Health Maintenance Organization (HMO)', 'Preferred Provider Organization (PPO)', 'Point of Service (POS)', 'High Deductible Health (HDHP)',
        'Short term Health Insurance', 'Gap Insurance']
    speech_output = 'You can go with a {} medical health insurance plan'.format(random.choice(plans))
    reprompt_text = "I said," + speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello, I am your recommendation assitant, your application has started! you can ask for your benefits or ask for help! First tell me your user id!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, I am your recommendation assitant! Tell me your user id!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "askid":
        return get_id_response(intent, session)
    elif intent_name == "askbenefit":
        return get_benefit_response()
    elif intent_name == "askservice":
        return get_service_response(intent, session)
    elif intent_name == "askrecommend":
        return get_recommend_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
