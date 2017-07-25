from oauth2client import client

scopes = ["https://www.googleapis.com/auth/forms", "https://www.googleapis.com/auth/script.external_request"]
flow = client.flow_from_clientsecrets('client_secret.json', scopes, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
auth_uri = flow.step1_get_authorize_url()
print(auth_uri)
