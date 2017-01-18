# import os
# import yaml

# path = ("/").join([os.path.dirname(os.path.dirname(__file__)), "settings", "pipeline.yml"])
# pipelinePath = {}

# if os.path.exists(path):
#     with open(path, 'r') as stream:
#         try:
#             pipelinePath = yaml.load(stream)["PATH_PIPELINE"]
#         except yaml.YAMLError as exc:
#             print(exc)

#     for eachPath in pipelinePath:
#         print eachPath

# else:
#     print "NOP"

# import yaml

# path = "D:/Dropbox/arPipeline/2000/data/project.yml"
# tmp_pipeline_paths = ""
# with open(path, 'r') as stream:

#     tmp_pipeline_paths = yaml.load(stream)

# print tmp_pipeline_paths

# def test(path):
#     return path + "WHAT"

# import sys
# print map(test, sys.path)
# print sys.path


import os
print os.path.splitext("hallo.haha")
