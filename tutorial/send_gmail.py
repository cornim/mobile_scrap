'''
Created on Sep 14, 2015

@author: corni
'''
# Import smtplib for the actual sending function
import smtplib
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import os.path
import webbrowser
import base64
import httplib2

def GenerateOAuth2String(username, access_token, base64_encode=True):
    """Generates an IMAP OAuth2 authentication string.
    
    See https://developers.google.com/google-apps/gmail/oauth2_overview
    
    Args:
      username: the username (email address) of the account to authenticate
      access_token: An OAuth2 access token.
      base64_encode: Whether to base64-encode the output.
    
    Returns:
      The SASL argument for the OAuth2 mechanism.
    """
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if base64_encode:
        auth_string = base64.b64encode(auth_string)
    return auth_string


fname = "cred.json"

credentials = ""
store = Storage(fname)
if os.path.isfile(fname):
    store.acquire_lock()
    credentials = store.locked_get()
    store.release_lock()
else:
    flow = flow_from_clientsecrets('client_secret.json',
                                   scope='https://mail.google.com/',
                                   redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    auth_code = raw_input('Enter the auth code: ')
    credentials = flow.step2_exchange(auth_code)
    store.acquire_lock()
    store.locked_put(credentials)
    store.release_lock()
    credentials.set_store(store)

user = 'cornelius.mund@gmail.com'
if credentials.access_token_expired:
    http = httplib2.Http()
    credentials.refresh(http)
auth_string = GenerateOAuth2String(user, credentials.access_token)


# Import the email modules we'll need
from email.mime.text import MIMEText

msg = MIMEText('Test')


# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'Test'
msg['From'] = 'cornelius.mund@gmail.com'
msg['To'] = 'cornelius.mund@d-fine.de'

# Send the message via our own SMTP server, but don't include the
# envelope header.
server = smtplib.SMTP('smtp.gmail.com:587')
#server.set_debuglevel(True)
server.ehlo()
server.starttls()
server.ehlo()
server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
server.sendmail('cornelius.mund@gmail.com', ['cornelius.mund@d-fine.de'], msg.as_string())
server.quit()