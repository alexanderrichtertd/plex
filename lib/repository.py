#*********************************************************************
# content   = repository
# version   = 0.1.0
# date      = 2019-10-06
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import json
import requests

from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)

REPO_DATA = Tank().user.data_user_path



#*********************************************************************
# GIT
def make_github_issue(title, body=None, assignee=REPO_DATA['username'], milestone=None, labels=None):
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_DATA['owner'], REPO_DATA['repository'])

    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (REPO_DATA['username'], REPO_DATA['password'])

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


