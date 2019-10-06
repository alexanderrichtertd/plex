#*********************************************************************
# content   = repository
# version   = 0.0.1
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import json
import requests

import pipelog
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = pipelog.init(script=TITLE)

repo_data = Tank().data_repository

# Authentication for user filing issue
# (read/write access to repository)
USERNAME = repo_data['username']
PASSWORD = repo_data['password']

# repository to add this issue
REPO_OWNER = repo_data['owner']
REPO_NAME  = repo_data['repository']


#*********************************************************************
# GIT
def make_github_issue(title, body=None, assignee=USERNAME, milestone=None, labels=None):
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)

    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)

    issue = {'title': title,
             'body': body,
             'assignee': assignee,
             'milestone': milestone,
             'labels': labels}

    # Add the issue to our repository
    repo = session.post(url, json.dumps(issue))

    if repo.status_code == 201:
        LOG.info('Successfully created Issue {}'.format(title))
    else:
        LOG.warning('Could not create Issue {}.\nResponse:{}'.format(title, repo.content))


#*********************************************************************
# TEST
# make_github_issue(title='Login Test', body='Body text', milestone=None, labels=['bug'])


