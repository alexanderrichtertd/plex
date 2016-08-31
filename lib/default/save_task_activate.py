   # try:
                #     mel.eval('file -removeReference -referenceNode "SCENE_' + s.TASK["shading"] + 'RN";')
                # except:
                #     LOG.error('FAIL : SAVE : Cant remove SCENE_' + s.TASK["shading"] + " reference **", exc_info=True) 

                # try:
                #     from scripts.SHD import uniteShaderGroup
                #     uniteShaderGroup.start()
                # except:
                #     LOG.error('FAIL : Unite Shader and Shader Group :', exc_info=True) 

                # sceneFile = mel.eval('file -q -l;') [1:]

                # for files in sceneFile:
                #     if files.endswith(s.FILE_FORMAT[os.environ["SOFTWARE"]]):
                #         tmpReference = os.path.basename(files).split(".")[0] + "RN"
                #         sceneReference.append(tmpReference)

                #         try:
                #             cmds.file(unloadReference=tmpReference)
                #         except:
                #             LOG.error('FAIL : SAVE : Reference not exists: ' + tmpReference, exc_info=True) 

