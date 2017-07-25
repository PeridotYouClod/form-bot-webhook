# form-bot-webhook

## How To Refresh Creds
1. Go to the Google cloud console and refresh the creds for ["Form-Fill"](https://console.cloud.google.com/apis/credentials/oauthclient/198153364328-sj0sculn16l8tqm0q2r1tq76u1vcl8q6.apps.googleusercontent.com?project=project-id-1420503723986652166)
2. Download the JSON file
3. Move the cred file to the same folder as this project name it "client_secret.json"
4. Run: `python2 auth_step1.py` if it fails check for changing scopes!
5. Follow the auth flow and get the code out at the end
6. Edit auth_step2.py to have your code in the "credentials = flow.step2_exchange('YOUR_CODE')"
7. Run: `python2 auth_step2.py`
8. Now you have a new cred file to update heroku
