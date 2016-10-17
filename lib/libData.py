#*************************************************************
# CONTENT       gets & sets data files
#
# AUTHOR        Alexander Richter
#*************************************************************

import json

#************************
# YAML
def setYmlFile(path, content):
	print "set YAML file"


def get YmlFile(path):
	print "Get YAML file"


#************************
# JSON
def setJsonFile(path, content):
    with open(path, 'w') as outfile:
        json.dump(content.__dict__, outfile)


def getJsonFile(path):
    with open(path, 'r') as outfile:
        return json.load(outfile)


