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
import datetime
import httplib2
from email.mime.text import MIMEText

class GmailSender(object):
    
    credentials = None
    server = None
    
    def GenerateOAuth2String(self, username, access_token, base64_encode=True):
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
    
    
    def load_oauth2_credentials(self, fname_secret, fname_creds):
        store = Storage(fname_creds)
        if os.path.isfile(fname_creds):
            store.acquire_lock()
            self.credentials = store.locked_get()
            store.release_lock()
        else:
            flow = flow_from_clientsecrets(fname_secret,
                                           scope='https://mail.google.com/',
                                           redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        
            auth_uri = flow.step1_get_authorize_url()
            webbrowser.open(auth_uri)
            auth_code = raw_input('Enter the auth code: ')
            self.credentials = flow.step2_exchange(auth_code)
            store.acquire_lock()
            store.locked_put(self.credentials)
            store.release_lock()
            self.credentials.set_store(store)
    
    def start_server(self):
        if self.credentials == None:
            self.load_oauth2_credentials('client_secret.json', "cred.json")
    
        user = 'cornelius.mund@gmail.com'
        if (self.credentials.token_expiry - datetime.datetime.utcnow()) < datetime.timedelta(minutes=2):
            http = httplib2.Http()
            self.credentials.refresh(http)
        auth_string = self.GenerateOAuth2String(user, self.credentials.access_token)
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        #server.set_debuglevel(True)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
        
    def stop_server(self):
        self.server.quit()
        
    
    def send_mail(self, text, subject = "", to_addr = 'cornelius.mund@gmail.com', from_addr = 'cornelius.mund@gmail.com'):        
        
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        
        self.server.sendmail(from_addr, [to_addr], msg.as_string())
        