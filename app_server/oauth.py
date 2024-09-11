from flask import Flask, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']  # Set this in Heroku environment variables

CLIENT_SECRETS_FILE = os.environ['GOOGLE_CLIENT_SECRETS']
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.readonly'  # Added email API scope
]

@app.route('/')
def index():
    return 'Welcome to the Calendar API! <a href="/authorize">Authorize</a>'

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=session['state'],
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Save the credentials for future use
    # You can save them to a file or a database
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

    return 'Authorization successful! You can now create calendar events.'

@app.route('/create_event')
def create_event():
    # Load credentials from token.json
    from google.oauth2.credentials import Credentials
    credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    # Create a sample event
    event = {
        'summary': 'Sample Event',
        'start': {
            'dateTime': '2023-10-01T10:00:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2023-10-01T11:00:00',
            'timeZone': 'America/Los_Angeles',
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return f'Event created: {event_result.get("htmlLink")}'

if __name__ == '__main__':
    app.run(port=8080)
