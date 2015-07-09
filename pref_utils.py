import os
import json

def saveUserInfo(username, accesskey):
    userinfo_filename = 'userinfo.json'

    jsonData = {
    'username' : username,
    'accesskey' : accesskey
    }

    with open(userinfo_filename, 'w') as outfile:
         json.dump(jsonData, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

def readUserInfo():
    userinfo_filename = 'userinfo.json'
    if not os.path.exists(userinfo_filename):
        return None

    data = None
    with open(userinfo_filename, 'r') as f:
        data = json.load(f)

    if not data is None:
        return (data['username'], data['accesskey'])
    else:
        return None

