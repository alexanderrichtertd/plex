#*********************************************************************
# content   = setup software attributes
# version   = 0.1.0
# date      = 2024-11-09
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
LOG = Tank().log.init(script=__name__)
DEFAULT_PATH = os.path.normpath(os.getenv('DATA_USER_PATH').split(';')[0] + '/tmp_img.jpg')


#*********************************************************************
# CLASS
class Software(tank.Singleton):

    _NAME = 'software'

    def setup(self):
        os.environ['SOFTWARE'] = self._NAME
        self._software_data = Tank().data_software
        self._version = self._software_data['version']
        self._path    = self._software_data['path']

        # RENDERER
        self._renderer      = self._software_data.get('renderer', '')
        self._renderer_path = self._software_data.get('renderer_path', '')


    def setup_env(self):
        LOG.debug('- {} -----------------------------------------------------'.format(self._NAME.upper()))

        sub_path = []
        software_path = []

        for each_path in os.environ['SOFTWARE_SRC_PATH'].split(';'):
            # if not each_path.endswith('software'): each_path = os.path.dirname(each_path)
            tmp_paths  = ('/').join([each_path, self._NAME])
            software_path.append(tmp_paths)
            tmp_folder = pipefunc.get_file_list(path=tmp_paths, exclude='.py', add_path=True)
            if not tmp_folder: continue
            sub_path.extend(tmp_folder)

        os.environ['SOFTWARE_PATH']     = (';').join(software_path)
        os.environ['SOFTWARE_SUB_PATH'] = (';').join(sub_path)
        LOG.debug("SOFTWARE_PATH: {}".format(os.environ['SOFTWARE_PATH']))

        # GET data
        self._software_data = Tank().data_software
        self._env = self._software_data.get('ENV', '')

        # ADD software ENV
        if(self._env):
            for env, content in self._env.items():
                if isinstance(content, list):
                    for each in content: Tank().add_env(env, each)
                else: Tank().add_env(env, content)

            LOG.debug('{}_ENV: {}'.format(self._NAME.upper(), self._env))



    #*********************************************************************
    # SOFTWARE
    def start(self, software, open_file=''):
        self._NAME = software

        self.setup()
        self.setup_env()

        cmd = self._software_data['start'].format(open_file)

        if open_file:
            if self._NAME == 'maya':
                cmd = '{} -file "{}"'.format(cmd, open_file)
            elif self._NAME == 'max' or self._NAME == 'houdini':
                cmd = '"{}" "{}"'.format(cmd, open_file)

        LOG.debug(cmd)
        subprocess.Popen(cmd, shell=True, env=os.environ)



    def __call__(self):
        LOG.info('SOFTWARE: {} {} - {}\n\
                  ENV: {}'.format(self._NAME, self._version, self._path, self._env))



    #*********************************************************************
    # VARIABLES
    @property
    def id(self):
        return id(self)

    @property
    def software(self):
        return self._NAME

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
        return Tank().data_project['EXTENSION'][self._NAME]

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
    # IS DCC
    @property
    def is_maya(self):
        return self.software == 'maya'

    @property
    def is_nuke(self):
        return self.software == 'nuke'

    @property
    def is_houdini(self):
        return self.software == 'houdini'

    @property
    def is_max(self):
        return self.software == 'max'


    #*********************************************************************
    # FUNCTION
    @property
    def scene_path(self):
        LOG.warning('NO software override found')

    def scene_save(self):
        LOG.warning('NO software override found')

    def scene_save_as(self, file):
        LOG.warning('NO software override found')

    def scene_open(self, file):
        LOG.warning('NO software override found')

    def scene_import(self, file):
        LOG.warning('NO software override found')


    #*********************************************************************
    # MENU
    def add_menu(self, menu_node):
        self.add_sub_menu = []
        self._software_data = Tank().data_software

        for menu_item in self._software_data['MENU']:
            try:    self.add_menu_item(menu_node, menu_item)
            except: LOG.error('SOFTWARE Menu couldnt be created', exc_info=True)

        if self._NAME == 'max':
            import MaxPlus
            main_menu = menu_node.Create(MaxPlus.MenuManager.GetMainMenu())
            for sub in self.add_sub_menu: sub.Create(main_menu, 0)

    def add_menu_item(self, menu_node, new_command):
        if   self._NAME == 'maya': import maya.cmds as cmds
        elif self._NAME == 'max' : import MaxPlus
        else:
            LOG.debug('CANT find software: {}'.format(self._NAME))
            return

        sub_menu = ''

        for keys, item in new_command.items():

            if isinstance(item, dict) or isinstance(item, list):
                if self._NAME == 'maya':
                    sub_menu = cmds.menuItem(p=menu_node, l=keys, sm=True)
                elif self._NAME == 'max':
                    MaxPlus.MenuManager.UnregisterMenu(unicode(keys))
                    sub_menu = MaxPlus.MenuBuilder(keys)
                    self.add_sub_menu.append(sub_menu)
                elif self._NAME == 'nuke':
                    sub_menu = menu_node.addMenu(keys)

                if sub_menu and isinstance(item, list):
                    for it in item:
                        self.add_menu_item(sub_menu, it)
                elif sub_menu: self.add_menu_item(sub_menu, item)

            else:
                if self._NAME == 'maya':
                    eval('cmds.{}'.format(item).format(menu_node))
                elif self._NAME == 'max':
                    import max_menu
                    eval('menu_node.{}'.format(item))
                elif self._NAME == 'nuke':
                    eval('menu_node.{}'.format(item))


    #*********************************************************************
    # SETUP
    # TODO: NEEDS to be DCC independent
    def scene_setup(self, setup_type, status='', default=True):
        import maya.cmds as cmds

        data_setup = Tank().data_software['SETUP']
        LOG.info(data_setup)
        new_setup  = []

        if default:
            new_setup += data_setup['DEFAULT']

        if status in data_setup:
            new_setup += data_setup[status]

        LOG.debug(new_setup)

        for setting in new_setup:
            for key, item in setting.items():
                # TODO: Maybe needs optVar option - will see
                render = "cmds.setAttr('{}', {})".format(key, item)

                try:    eval(render)
                except: LOG.error('Scene Setup is not executable: {}'.format(render), exc_info=True)

    #******************************************************************************
    # SNAPSHOT
    def viewport_snapshot(img_path=DEFAULT_PATH):
        LOG.info("viewport_snapshot")

    def render_snapshot(img_path=DEFAULT_PATH):
        LOG.info("render_snapshot")

    #*********************************************************************
    # PRINT
    def print_header(self):
        if self._NAME == 'max': return

        space = (20-int(len(os.getenv('PROJECT_NAME'))/2)) - 1

        # project name
        print('')
        print(chr(124) + chr(151)*38 + chr(124))
        print(chr(124) + ' ' * space + os.getenv('PROJECT_NAME') + ' ' * space + chr(124))
        print(chr(124) + chr(151)*38 + chr(124))

        # user name
        print ('\n' + ' '*12 + 'Welcome ' + getpass.getuser() + '\n')

        print('PATH')

        self.print_checked_header('img')
        self.print_checked_header('data')
        self.print_checked_header('lib')
        self.print_checked_header('lib/apps')
        self.print_checked_header('software/{}'.format(self._NAME))
        self.print_checked_header('software/{}/icons'.format(self._NAME))
        self.print_checked_header('software/{}/plugins'.format(self._NAME))
        self.print_checked_header('software/{}/scripts'.format(self._NAME))

        if self._NAME == 'maya':
            self.print_checked_header('software/{}/shelf'.format(self._NAME))
        if self._NAME == 'nuke':
            self.print_checked_header('software/{}/gizmos'.format(self._NAME))

        print('') # ********************

        print('SCENE')
        # scripts from software/MENU
        for menu_item in self._software_data['MENU']:
            for key in menu_item:
                if key == 'break': continue
                self.print_checked_header(key)

        print('') # ********************


    def print_checked_header(self, content, func=''):
        try:
            func
            print('  {} ON  - {}'.format(chr(149), content))
        except:
            LOG.debug('  OFF - {}'.format(content))
            print('  {} OFF - {}'.format(chr(149), content))



