#!/usr/bin/env python
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib
import urllib.request, urllib.error
import json
import os

from flask import Flask, request, make_response

import httplib2

from apiclient import discovery
from oauth2client import client,tools
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
    print("Request: %s" % json.dumps(req, indent=2))

    res = processRequest(req)

    return _makeJsonResponse(res)

def _makeJsonResponse(res):
    res = json.dumps(res, indent=2)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

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
            print('Success!')

    except Exception as e:
        # failure before the script started executing.
        print("failed because", e)

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
