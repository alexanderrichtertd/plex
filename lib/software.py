#*********************************************************************
# content   = setup software attributes
# version   = 0.1.0
# date      = 2019-12-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import getpass
import subprocess

import pipefunc

import tank
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# CLASS
class Software(tank.Singleton):

    def setup(self, software=os.getenv('SOFTWARE')):
        if not software: raise OSError ('STOP PROCESS', 'SOFTWARE couldnt be found.')

        self._software = software.lower()
        self._software_data = Tank().data_software

        self._version = self._software_data['version']
        self._path    = self._software_data['path']

        # RENDERER
        self._renderer      = self._software_data.get('renderer', '')
        self._renderer_path = self._software_data.get('renderer_path', '')

    def setup_env(self):
        LOG.debug('- {} -----------------------------------------------------'.format(self._software.upper()))

        sub_path = []
        software_path = []

        for each_path in os.environ['SOFTWARE_SRC_PATH'].split(';'):
            # if not each_path.endswith('software'): each_path = os.path.dirname(each_path)
            tmp_paths  = ('/').join([each_path, self._software])
            software_path.append(tmp_paths)
            tmp_folder = pipefunc.get_file_list(path=tmp_paths, exclude='.py', add_path=True)
            if not tmp_folder: continue
            sub_path.extend(tmp_folder)

        os.environ['SOFTWARE']          = self._software.upper()
        os.environ['SOFTWARE_PATH']     = (';').join(software_path)
        os.environ['SOFTWARE_SUB_PATH'] = (';').join(sub_path)
        LOG.debug("SOFTWARE_PATH: {}".format(os.environ['SOFTWARE_PATH']))

        # GET data
        self._software_data = Tank().data_software
        self._env = self._software_data.get('ENV', '')

        # ADD software ENV
        if(self._env):
            for env, content in self._env.iteritems():
                if isinstance(content, list):
                    for each in content: Tank().add_env(env, each)
                else: Tank().add_env(env, content)

            LOG.debug('{}_ENV: {}'.format(self._software.upper(), self._env))


    #*********************************************************************
    # SOFTWARE
    def start(self, software, open_file=''):
        try:    tmp_software = self._software
        except: tmp_software = ''

        self.setup(software)
        self.setup_env()

        cmd = self._software_data['start'].format(open_file)

        if open_file:
            if self._software == 'maya':
                cmd = '{} -file "{}"'.format(cmd, open_file)
            if self._software == 'max' or self._software == 'houdini':
                cmd = '"{}" "{}"'.format(cmd, open_file)

        LOG.debug(cmd)
        subprocess.Popen(cmd, shell=True, env=os.environ)

        if tmp_software: self.setup(tmp_software)


    def __call__(self):
        LOG.info('SOFTWARE: {} {} - {}\n\
                  ENV: {}'.format(self._software, self._version, self._path, self._env))


    #*********************************************************************
    # VARIABLES
    @property
    def id(self):
        return id(self)

    @property
    def software(self):
        return self._software

    @property
    def version(self):
        return self._version

    @property
    def path(self):
        return self._path

    @property
    def data(self):
        return self._software_data

    @property
    def extension(self):
        return Tank().data_templates['EXTENSION'][self._software]

    @property
    def menu(self):
        return self._software_data['MENU']

    @property
    def env(self):
        return self._env

    @property
    def renderer(self):
        return self._renderer

    @property
    def renderer_path(self):
        return self._renderer_path


    #*********************************************************************
    # FUNCTION
    @property
    def scene_path(self):
        if self._software == "maya":
            import pymel.core as pm
            return pm.sceneName()
        elif self._software == "nuke":
            import nuke
            return nuke.root().knob('name').value()
        elif self._software == "max":
            import MaxPlus
            return MaxPlus.Core.EvalMAXScript("maxFilePath + maxFileName").Get()
        elif self._software == "houdini":
            print("file->houdini")
            return ''
        else: LOG.warning('NO scene returned: No software cmd found')
        return scene_path

    def scene_save(self):
        if self._software == "maya":
            import pymel.core as pm
            return pm.saveFile(file)
        elif self._software == "nuke":
            import nuke
            return nuke.scriptSave()
        elif self._software == "max":
            import MaxPlus
            return MaxPlus.FileManager.Save()
        elif self._software == "houdini":
            print("file->houdini")
            return ''
        else: LOG.warning('NO scene returned: No software cmd found')

    def scene_save_as(self, file, setup_scene=False):
        if setup_scene: self.scene_setup(file)

        if self._software == "maya":
            import pymel.core as pm
            return pm.saveAs(file)
        elif self._software == "nuke":
            import nuke
            nuke.scriptSaveAs(file)
        elif self._software == "max":
            import MaxPlus
            return MaxPlus.FileManager.Save(file)
        elif self._software == "houdini":
            print("file->houdini")
            return ''
        else: LOG.warning('NO scene returned: No software cmd found')

    def scene_open(self, file):
        if self._software == "maya":
            import pymel.core as pm
            return pm.openFile(file, force=True)
        elif self._software == "nuke":
            import nuke
            return nuke.scriptOpen(file)
        elif self._software == "max":
            import MaxPlus
            return MaxPlus.FileManager.Open(file)
        elif self._software == "houdini":
            print("file->houdini")
            return ''
        else: LOG.warning('NO scene returned: No software cmd found')

    def scene_import(self, file):
        pass

    def scene_setup(self, file):
        if self._software == "maya":
            import maya_utils
            maya_utils.setup_scene(file)
        else: LOG.warning('NO scene returned: No software cmd found')


    #*********************************************************************
    # MENU
    def add_menu(self, menu_node):
        self.add_sub_menu = []
        self._software_data = Tank().data_software

        for menu_item in self._software_data['MENU']:
            try:    self.add_menu_item(menu_node, menu_item)
            except: LOG.error('SOFTWARE Menu couldnt be created', exc_info=True)

        if self._software == 'max':
            import MaxPlus
            main_menu = menu_node.Create(MaxPlus.MenuManager.GetMainMenu())
            for sub in self.add_sub_menu: sub.Create(main_menu, 0)

    def add_menu_item(self, menu_node, new_command):
        if   self._software == 'maya': import maya.cmds as cmds
        elif self._software == 'max' : import MaxPlus
        elif self._software == 'nuke': pass
        else:
            LOG.debug('CANT find software: {}'.format(software))
            return

        sub_menu = ''

        for keys, item in new_command.iteritems():

            if isinstance(item, dict) or isinstance(item, list):
                if self._software == 'maya':
                    sub_menu = cmds.menuItem(p=menu_node, l=keys, sm=True)
                elif self._software == 'max':
                    MaxPlus.MenuManager.UnregisterMenu(unicode(keys))
                    sub_menu = MaxPlus.MenuBuilder(keys)
                    self.add_sub_menu.append(sub_menu)
                elif self._software == 'nuke':
                    sub_menu = menu_node.addMenu(keys)

                if sub_menu and isinstance(item, list):
                    for it in item:
                        self.add_menu_item(sub_menu, it)
                elif sub_menu: self.add_menu_item(sub_menu, item)

            else:
                LOG.info('{} - {} - {}'.format(menu_node, keys, item))
                if self._software == 'maya':
                    eval('cmds.{}'.format(item).format(menu_node))
                elif self._software == 'max':
                    import max_menu
                    eval('menu_node.{}'.format(item))
                elif self._software == 'nuke':
                    eval('menu_node.{}'.format(item))


    #*********************************************************************
    # SETUP
    def set_scene(self):
        pass

    def set_rendersettings(self, status):
        pass


    #*********************************************************************
    # PRINT
    def print_header(self):
        if self._software == 'max': return

        space = (20-int(len(os.getenv('PROJECT_NAME'))/2)) - 1

        # project name
        print('')
        print(chr(218) + chr(196)*38 + chr(191))
        print(chr(179) + ' '*space + os.getenv('PROJECT_NAME') + ' '*space + chr(179))
        print(chr(192) + chr(196)*38 + chr(217))

        # user name
        print ('\n' + ' '*12 + 'Welcome ' + getpass.getuser() + '\n')

        print('PATHS')
        print('  {} ON  - img'.format(chr(254)))
        print('  {} ON  - lib'.format(chr(254)))
        print('  {} ON  - data'.format(chr(254)))
        print('  {} ON  - lib/utils'.format(chr(254)))
        print('  {} ON  - lib/classes'.format(chr(254)))
        print('  {} ON  - software/{}'.format(chr(254), self._software))
        print('  {} ON  - software/{}/scripts'.format(chr(254), self._software))
        print('  {} ON  - software/{}/plugins'.format(chr(254), self._software))
        if self._software == 'maya':
            print('  {} ON  - software/{}/shelf'.format(chr(254), self._software))
        if self._software == 'nuke':
            print('  {} ON  - software/{}/gizmos'.format(chr(254), self._software))

        print('') # ********************

        print('SCRIPTS')
        # scripts from software/MENU
        for menu_item in self._software_data['MENU']:
            for key in menu_item:
                if key == 'break': continue
                print('  {} ON  - {}'.format(chr(254), key))

        print('') # ********************


    def print_checked_header(self, text, content, func):
        try:
            func
            print('  {} ON  - {}: {}'.format(chr(254), text, content))
        except:
            LOG.debug('  OFF - {}: {}'.format(content))
            print('  {} OFF - {}: {}'.format(chr(254), text, content))



