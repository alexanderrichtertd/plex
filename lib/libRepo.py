#*********************************************************************
# content   = project data
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import json
import base64
import requests

import libData
import libLog


#************************
# VAR
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

repo_data = libData.get_data()['project']['REPOSITORY']

# Authentication for user filing issue
# (read/write access to repository)
USERNAME = repo_data['username']
PASSWORD = repo_data['password']

# repository to add this issue
REPO_OWNER = repo_data['owner']
REPO_NAME  = repo_data['repository']


#************************
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
    r = session.post(url, json.dumps(issue))

    if r.status_code == 201:
        LOG.info('Successfully created Issue {}'.format(title))
    else:
        LOG.warning('Could not create Issue {}.\nResponse:{}'.format(title, r.content))


#************************
# TEST
# make_github_issue(title='Login Test', body='Body text', milestone=None, labels=['bug'])


