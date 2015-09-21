import yaml
import requests_oauthlib
import requests
import urllib.parse
import os.path
import xmltodict
import time
import os
from collections import OrderedDict
import unicodecsv
import pickle
import time

#read in credentials
with open("credentials.yml", 'r') as ymlfile:
    creds = yaml.load(ymlfile)

key = creds['consumer_key']
secret = creds['consumer_secret']

#yahoo OAuth URLs
request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
authorization_base_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'
access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
callback = 'oob'

def user_auth():
    #make the initial oauth call
    oauth = requests_oauthlib.OAuth1(key, client_secret=secret, callback_uri=callback)
    r = requests.post(url=request_token_url, auth=oauth)

    #parse the response
    response = urllib.parse.parse_qsl(r.content)
    #owner_key = response.get('oauth_token')[0]
    #owner_secret = response.get('oauth_token_secret')[0]
    owner_key = bytes.decode(response[0][1])
    owner_secret = bytes.decode(response[1][1])

    #get the verification code (interactive)
    authorize_url = authorization_base_url + '?oauth_token='
    authorize_url = authorize_url + owner_key
    print( 'Please go here and authorize (if in PuTTY, use mouse to highlight URL to copy to clipboard):\n',authorize_url)
    verifier = input('Please input the verifier: ')

    #get the final token
    oauth = requests_oauthlib.OAuth1Session(key, client_secret=secret,
        resource_owner_key=owner_key, resource_owner_secret=owner_secret, verifier=verifier)

    #write response to yaml
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    with open('auth.yml', 'w') as outfile:
        outfile.write(yaml.dump(oauth_tokens))

def session_from_auth(auth_dict):
    #print oauth_tokens
    res_owner_key = auth_dict['oauth_token']
    res_owner_secret  = auth_dict['oauth_token_secret']
    return requests_oauthlib.OAuth1Session(
        key,
        client_secret=secret,
        resource_owner_key=res_owner_key,
        resource_owner_secret=res_owner_secret
    )

def read_stored_auth():
    with open("auth.yml", 'r') as ymlfile:
        final_auth = yaml.load(ymlfile)
    return final_auth


def test_stored_auth():
    if os.path.exists("auth.yml"):
        return (time.time() - os.stat("auth.yml").st_mtime) < 3300 #55 minutes
    return False


def yahoo_session():
    if(test_stored_auth()):
        return session_from_auth(read_stored_auth())
    else:
        user_auth()
        return session_from_auth(read_stored_auth())

def api_query(y_session, query):
    r = y_session.get(query)
    time.sleep(1)
    return xmltodict.parse(r.content)

def data_pickle(data, filename):
    with open(filename,'wb') as f:
        pickle.dump(data,f,pickle.HIGHEST_PROTOCOL)

def data_to_csv(target_dir, data_to_write, desired_name):
    """Convenience function to write a dict to CSV with appropriate parameters."""
    #generate directory if doesn't exist
    global d
    if len(data_to_write) == 0:
        return None
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if type(data_to_write) == dict:
        #order dict by keys
        d = OrderedDict(sorted(data_to_write.items()))
        keys = d.keys()
    if type(data_to_write) == list:
        d = data_to_write
        keys = data_to_write[0].keys()
    with open("%s/%s.csv" % (target_dir, desired_name), 'wb') as f:
        dw = unicodecsv.DictWriter(f, keys, dialect='ALM')
        dw.writeheader()
        if type(data_to_write) == dict:
            dw.writerow(d)
        if type(data_to_write) == list:
            dw.writerows(d)
    f.close()
