"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from botocore.vendored import requests
from difflib import SequenceMatcher

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>' + output + '</speak>'
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

def get_welcome_response():
    session_attributes = {}
    card_title         = "Welcome"
    speech_output      = "Welcome to the Brennan Skill"
    reprompt_text      = None
    should_end_session = True
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Brennan skill. "
    
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def spellOut(input):
    return '<say-as interpret-as="spell-out">' + input + '</say-as>'


def pause(seconds):
    return '<break time="' + str(seconds) + 's"/>'


def brennanRequest(address):
    print("Brennan request - "  + address)
    return requests.get("http://dpgwynne.ddns.net:8000/b2cgi.fcgi?" + address)


def brennanVolumeRequest(delta):
    data = brennanRequest("status").json()
    volume = int(data['volume'])

    if volume + delta > 0 and volume + delta < 64:
        brennanRequest("vol"+str(volume + delta))


def brennanIdRequest(id):
    brennanRequest("playID&" + id)


def response(intent, session, text):
    session_attributes = {}
    reprompt_text      = None
    speech_output      = text
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def play(intent, session):
    brennanRequest("play")

    verb = ''

    if intent['name'] == "Play":
        verb = "playing"
    elif intent['name'] == "Pause":
        verb = "pausing"
    elif intent['name'] == "Stop":
        verb = "stopping"

    return response(intent, session, 'Brennan ' + verb)


def closest(collection, text):
    id = None

    bestScore = 0.0
    bestEntry = ''

    for entry in collection.keys():
        score = SequenceMatcher(None, entry, text).ratio()

        #if score > 0.7:
        #    print ("Entry [" + entry + "] got [" + str(score) + "]")

        if score > bestScore:
            bestScore = score
            bestEntry = entry 
            id = str(collection[entry])

    #print("Best score:"  + str(bestScore))

    return id, bestEntry


def playAlbum(intent, session):
    if 'slots' in intent and 'albumName' in intent['slots']:
        albumName = intent['slots']['albumName']['value']

        albums  = {}
        artists = {}

        permittedChars = "0123456789abcdefghijklmnopqrstuvwxyz "

        offset = 0
        count  = 0

        while offset == 0 or count == 500:
            data = brennanRequest("search&artists=N&tracks=N&radio=N&count=500&offset=" + str(offset)).json()

            for item in data:
                if item['id'] >= 1000000 and item['id'] < 2000000:
                    albums[" ".join("".join(c for c in item['album'].lower() if c in permittedChars).split())] = item['id']
                    artists[str(item['id'])] = item['artist']
                    count = count + 1

            offset = offset + 500
            count  = 0

        print("Loaded " + str(len(albums)) + " albums.")

        id, album = closest(albums, albumName.lower())

        if id is not None:
            brennanIdRequest(id)
            return response(intent, session, 'Brennan playing album ' + album + ' by ' + artists[id])
        else:
            return response(intent, session, 'I dont know the album ' + albumName)
        
    else:
        return response('I dont know which album you want me to play.')


def nextTrack(intent, session):
    brennanRequest("next")
    return response(intent, session, 'Brennan Next track')


def backTrack(intent, session):
    brennanRequest("back")
    return response(intent, session, 'Brennan Previous track')


def volumeUp(intent, session):
    brennanVolumeRequest(5)
    return response(intent, session, 'Brennan Volume Up')


def volumeReallyUp(intent, session):
    brennanVolumeRequest(10)
    return response(intent, session, 'Brennan Volume Really Up')


def volumeDown(intent, session):
    brennanVolumeRequest(-5)
    return response(intent, session, 'Brennan Volume Down')


def volumeReallyDown(intent, session):
    brennanVolumeRequest(-10)
    return response(intent, session, 'Brennan Volume Really Down')

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Play" or intent_name == "Stop" or intent_name == "Pause":
        return play(intent, session)
    elif intent_name == "PlayAlbum":
        return playAlbum(intent, session)
    elif intent_name == "Next":
        return nextTrack(intent, session)
    elif intent_name == "Back":
        return backTrack(intent, session)
    elif intent_name == "VolumeUp":
        return volumeUp(intent, session)
    elif intent_name == "VolumeReallyUp":
        return volumeReallyUp(intent, session)
    elif intent_name == "VolumeDown":
        return volumeDown(intent, session)
    elif intent_name == "VolumeReallyDown":
        return volumeReallyDown(intent, session)
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
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.2351daec-3dae-418d-bd81-c362a95baa0e"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


if __name__ == "__main__":
    # execute only if run as a script
    intent = {'name' : 'PlayAlbum', 'slots' : {'albumName' : {'value' : 'joshua tree'}}}
    #intent = {'name' : 'Play'}
    session = {}

    print(playAlbum(intent, session))