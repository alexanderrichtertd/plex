#*************************************************************
# CONTENT       methods to use git
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import json
import base64
import requests

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'alexanderrichter'
PASSWORD = 'donttrustyou789'
PASSWORD = 'ZG9udHRydXN0eW91Nzg5'

# The repository to add this issue to
REPO_OWNER = 'alexanderrichter'
REPO_NAME  = 'arPipeline'

def make_github_issue(title, body=None, assignee=USERNAME, milestone=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)

    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, base64.b64encode(PASSWORD))
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

# make_github_issue(title='Login Test', body='Body text', milestone=None, labels=['bug'])


