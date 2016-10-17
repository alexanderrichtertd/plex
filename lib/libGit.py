



import json
import requests

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'alexanderrichter'
USERNAME = 'cf571c58978dbf0c31726da38583837b06fc7da84a6c29e0fd8b86764405095e'
PASSWORD = 'donttrustyou789'
PASSWORD = 'a3992b2b7d8f2fe207c61cb0f5736c26c9484b5d73ee5fee0622a6c3639411d4'

# The repository to add this issue to
REPO_OWNER = 'alexanderrichter'
REPO_NAME  = 'arPipeline'

def make_github_issue(title, body=None, assignee=USERNAME, milestone=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    #url = 'https://github.com/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    print url
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Create our issue
    issue = {'title': title,
             'body': body,
             'assignee': assignee,
             'milestone': milestone,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print 'Successfully created Issue "%s"' % title
    else:
        print 'Could not create Issue "%s"' % title
        print 'Response:', r.content

make_github_issue(title='Login Test', body='Body text', milestone=None, labels=['bug'])




import uuid
import hashlib

def hash_password(password):
    # uuid is used to generate a random number
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password):
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

# hashed_user = hash_password(USERNAME)
# hashed_password = hash_password(PASSWORD)
# print('USERNAME: ' + hashed_user)
# print('PASSWORD: ' + hashed_password)
