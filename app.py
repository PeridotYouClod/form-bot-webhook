#!/usr/bin/env python

from __future__ import print_function
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from oauth2client.client import OAuth2WebServerFlow

import tempfile

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/script.scriptapp'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Quickstart'

# Flask app should start in global layout
app = Flask(__name__)
credentials = None


@app.route('/login', methods=['GET'])
def login():
    credentials = get_credentials()

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    # ID of the script to call. Acquire this from the Apps Script editor,
    SCRIPT_ID = 'MYjwzHYAJOd3JrUyFsgHBV5sYkudgbe9Q'
    # Initialize parameters for function call.
    request = {
        "function": "myFunction"
        }

    try:
        http = credentials.authorize(httplib2.Http())

        service = discovery.build('script', 'v1', http=http)
        # Make the request.
        response = service.scripts().run(body=request,
                scriptId=SCRIPT_ID).execute()

        # Print results of the request.
        if 'error' in response:
            # The API executed, but the script returned an error.
            error = response['error']['details'][0]
            print("Script error! Message: {0}".format(error['errorMessage']))
        else:
            # Here, the function returns an array of strings.
            #sheetNames = response['response'].get('result')
            print('Success!')
            #for name in sheetNames:
            #    print("\t{0}".format(name))

    except Exception as e:
        # The API encountered a problem before the script started executing.
        print("failed because", e)

'''
def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
'''

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    secretFile = open("client_secret.json", 'w')
    secretFile.truncate()
    secretFile.write(os.environ['secret'])
    secretFile.close()
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid or True:
        flow = client.flow_from_clientsecrets("client_secret.json", SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, None)
        print('Storing credentials to ' + credential_path)
    return credentials

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')