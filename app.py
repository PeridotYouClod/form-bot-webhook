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
SCOPES = ['https://www.googleapis.com/auth/script.scriptapp',
          'https://www.googleapis.com/auth/forms']

CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Quickstart'

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=2))

    res = processRequest(req)

    res = json.dumps(res, indent=2)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/pricenow', methods=['POST'])
def pricenow():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=2))

    res = processPricenow(req)

    res = json.dumps(res, indent=2)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processPricenow(req):
    params = req["result"]["parameters"]
    print("processPricenow: %s", json.dumps(params, indent=2))
    print("unit-currency: %s",  json.dumps(params["unit-currency"], indent=2))
    print("Amount: %s", params["unit-currency"]["amount"])
    newMoney = float(params["unit-currency"]["amount"]) * 2.0
    print("newMoney: %s", newMoney)
    speech =  "This is not right but $" + str(newMoney)
    print("speech:  %s", speech)
    retObj = {
        "speech": speech,
        "displayText": speech,
        "source": "Formbot-Webhook-pricenow"        
    }
    print("retObj:  %s", json.dumps(retObj, indent=2))
    return retObj

def processRequest(req):
    print("processRequest: " + json.dumps(req["result"]["parameters"], indent=2))
    # Initialize parameters for function call.
    request = {
        "function": "fillForm",
        "parameters": [req["result"]["parameters"]]
    }
    try:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())

        service = discovery.build('script', 'v1', http=http)
        # Make the request.
        response = service.scripts().run(body=request,
                scriptId=os.environ['scriptId']).execute()

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
        # failure before the script started executing.
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
    secretFile = open("drive-python-quickstart.json", 'w')
    secretFile.write(os.environ['credential'])
    secretFile.close()

    store = Storage("drive-python-quickstart.json")
    credentials = store.get()
    return credentials

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
