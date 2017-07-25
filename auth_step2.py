from oauth2client import client
from oauth2client.file import Storage

scopes = ["https://www.googleapis.com/auth/forms", "https://www.googleapis.com/auth/script.external_request"]

flow = client.flow_from_clientsecrets('client_secret.json', scopes, redirect_uri='urn:ietf:wg:oauth:2.0:oob')

credentials = flow.step2_exchange('YOUR_CODE')
storage = Storage('generated_creds_for_heroku.json')
storage.put(credentials)
