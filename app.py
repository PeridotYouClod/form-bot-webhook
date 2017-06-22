#!/usr/bin/env python
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib
import urllib.request, urllib.parse, urllib.error
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
APIAI_TO_ID = {'temperature':"GroveTempHumD0/temperature",
               "humidity": "GroveTempHumD0/humidity"}



# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request: %s" % json.dumps(req, indent=2))

    res = processRequest(req)

    return _makeJsonResponse(res)

@app.route('/pricenow', methods=['POST'])
def pricenow():
    req = request.get_json(silent=True, force=True)

    print("Request: %s" % json.dumps(req, indent=2))

    res = processPricenow(req)

    return _makeJsonResponse(res)

@app.route('/sensorbot', methods=['POST'])
def sensorbot():
    req = request.get_json(silent=True, force=True)
    print("Request: %s" % json.dumps(req, indent=2))

    res = processSensorbot(req)

    return _makeJsonResponse(res)

def _makeJsonResponse(res):
    res = json.dumps(res, indent=2)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processSensorbot(req):
    root = "https://us.wio.seeed.io/v1/node/"
    access = "?access_token=" + os.environ['wioLink_access_token']
    print("Url: %sresources%s" % (root, access) )
    params = req["result"]["parameters"]
    print("params: %s" % params)
    sensors = params["sensors"]
    print("sensors: %s" % sensors)
    urls = []
    '''
    list(map(
        lambda sensor: APIAI_TO_ID[sensor]
    ))
    '''

    for sensor in sensors:
        urls.append(APIAI_TO_ID[sensor])
        print(APIAI_TO_ID[sensor])
    print("urls: %s" % urls)
    results = []
    for url in urls:
        builtUrl = root + url + access
        result = urllib.request.urlopen(builtUrl).read()
        jsonObj = json.loads(result)
        results.append(jsonObj)
        print(jsonObj)
    print("results: %s" % results)
    speech = ""
    for result in results:
        if 'humidity' in result:
            speech += "The Humidity is %s" % (result["humidity"])
        if 'celsius_degree' in result:
            speech += " The temperature is %s degrees celsius." % (result["celsius_degree"])
        print(speech)
#     response = requests.get(url + os.environ['wioLink_access_token'])
#     jsonObj = response.json()
#     print(json.dumps(jsonObj, indent=2))
#     speech =  "The Humidity is %s" % (jsonObj["humidity"])
    retObj = {
        "speech": speech,
        "displayText": speech,
        "source": "Formbot-Webhook-sensorbot"
    }
    print("retObj:  %s" % json.dumps(retObj, indent=2))
    return retObj

def processPricenow(req):
    params = req["result"]["parameters"]
    print("processPricenow: %s" % json.dumps(params, indent=2))
    lastYearInMap = 2016
    currentDollar =  CONVERSION_TABLE[lastYearInMap]
    if "date" in params:
        oldYear = int(params["date"])
    else:
        yearDiff = int(params["duration"]["amount"])
        oldYear = lastYearInMap - yearDiff
    oldYear = oldYear if oldYear >= 1913 else 1913
    ratio = currentDollar / CONVERSION_TABLE[oldYear]
    inputMoney = float(params["unit-currency"]["amount"])
    newMoney = inputMoney * ratio
    speech =  "In %s $%.2f was worth $%.2f" % (oldYear,inputMoney, newMoney)
    retObj = {
        "speech": speech,
        "displayText": speech,
        "source": "Formbot-Webhook-pricenow"
    }
    print("retObj:  %s" % json.dumps(retObj, indent=2))
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

CONVERSION_TABLE = {
    1913:1.00,
    1914:1.01,
    1915:1.02,
    1916:1.10,
    1917:1.29,
    1918:1.53,
    1919:1.75,
    1920:2.02,
    1921:1.81,
    1922:1.70,
    1923:1.73,
    1924:1.73,
    1925:1.77,
    1926:1.79,
    1927:1.76,
    1928:1.73,
    1929:1.73,
    1930:1.69,
    1931:1.54,
    1932:1.38,
    1933:1.31,
    1934:1.35,
    1935:1.38,
    1936:1.40,
    1937:1.45,
    1938:1.42,
    1939:1.40,
    1940:1.41,
    1941:1.48,
    1942:1.65,
    1943:1.75,
    1944:1.78,
    1945:1.82,
    1946:1.97,
    1947:2.25,
    1948:2.43,
    1949:2.40,
    1950:2.43,
    1951:2.63,
    1952:2.68,
    1953:2.70,
    1954:2.72,
    1955:2.71,
    1956:2.75,
    1957:2.84,
    1958:2.92,
    1959:2.94,
    1960:2.99,
    1961:3.02,
    1962:3.05,
    1963:3.09,
    1964:3.13,
    1965:3.18,
    1966:3.27,
    1967:3.37,
    1968:3.52,
    1969:3.71,
    1970:3.92,
    1971:4.09,
    1972:4.22,
    1973:4.48,
    1974:4.98,
    1975:5.43,
    1976:5.75,
    1977:6.12,
    1978:6.59,
    1979:7.33,
    1980:8.32,
    1981:9.18,
    1982:9.75,
    1983:10.06,
    1984:10.49,
    1985:10.87,
    1986:11.07,
    1987:11.47,
    1988:11.95,
    1989:12.53,
    1990:13.20,
    1991:13.76,
    1992:14.17,
    1993:14.60,
    1994:14.97,
    1995:15.39,
    1996:15.85,
    1997:16.21,
    1998:16.46,
    1999:16.83,
    2000:17.39,
    2001:17.89,
    2002:18.17,
    2003:18.59,
    2004:19.08,
    2005:19.73,
    2006:20.36,
    2007:20.94,
    2008:21.75,
    2009:21.67,
    2010:22.03,
    2011:22.72,
    2012:23.19,
    2013:23.53,
    2014:23.91,
    2015:23.94,
    2016:24.05
}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
