from py3pin.Pinterest import Pinterest
import json

credentials = json.loads(open('cookies/credentials.json').read())['pinterest']

pinterest = Pinterest(email=credentials['email'],
                      password=credentials['password'],
                      username=credentials['username'],
                      cred_root='cookies')
