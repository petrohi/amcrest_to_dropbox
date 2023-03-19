#!/usr/bin/env python3

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

DROPBOX_APP_KEY = os.environ['DROPBOX_APP_KEY']

auth_flow = DropboxOAuth2FlowNoRedirect(DROPBOX_APP_KEY, use_pkce=True, token_access_type='offline')

authorize_url = auth_flow.start()
print('1. Go to: ' + authorize_url)
print('2. Click \"Allow\" (you might have to log in first).')
print('3. Copy the authorization code.')
auth_code = input('Enter the authorization code here: ').strip()

try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print('Error: %s' % (e,))
    exit(1)

with dropbox.Dropbox(oauth2_refresh_token=oauth_result.refresh_token, app_key=DROPBOX_APP_KEY) as dbx:
    print(dbx.users_get_current_account().email)

print(oauth_result.refresh_token)