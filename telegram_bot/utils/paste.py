from urllib.parse import urlencode
from urllib.request import Request, urlopen

import requests

# PASTE_URL = 'http://paste.nekmo.com/api/'
PASTE_URL = 'https://dpaste.de/api/'
PASTE_TIME = 3600

def paste(text):
    request = requests.post(PASTE_URL, data={
        'content': text.encode(encoding='utf-8'),
        'lexer': 'plain',
        'format': 'url',
        'expires': str(PASTE_TIME),
    })
    return request.text
