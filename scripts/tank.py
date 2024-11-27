#*********************************************************************
# content   = main hub
# date      = 2024-11-25
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import getpass
import webbrowser

import pipelog
import pipefunc

LOG = pipelog.init(script=__name__)


#*********************************************************************
# CLASS
class Tank(pipefunc.Singleton):

    @property
    def software(self):
        """ Get the current software object based on the environment variable.
            RETURN: software class e.g. maya_dcc.Maya()
        """
        module_name = f"{self.software_name}_dcc" if self.software_name != 'software' else 'software'
        class_name = self.software_name.title()

        try:
            module = __import__(module_name, fromlist=[class_name])
            return getattr(module, class_name)()
        except ImportError:
            from software import Software
            return Software()

    @property
    def software_name(self):
        return os.environ.get('SOFTWARE', 'software')

    @property
    def context(self):
        return self.software.context

    @property
    def log(self):
        import pipelog
        return pipelog.init
    
    @property
    def LOG(self):
        return self.log.init(script=__name__)
   
    @property
    def announcement(self):
        # announcement order: overwrite than pipeline or project 
        return self.config_pipeline['announcement'] if self.config_project['announcement'] == 'None' or self.config_pipeline['announcement_overwrite'] else self.config_project['announcement']
    

    #*********************************************************************
    # CONFIG
    @property
    def config(self):
        return self.get_config()

    @property
    def config_project(self):
        return self.get_config('project')
    
    @property
    def config_pipeline(self):
        return self.get_config(file_name='pipeline', file_dir=self.paths['config'])

    @property
    def config_software(self):
        return self.get_config(f'software/{self.software_name}')


    #*********************************************************************
    # CONFIG: Get & Set
    def get_config(self, file_name='', file_dir='', user_id=getpass.getuser()):
        if not file_dir: file_dir = self.paths['config_project']
        file_dir = file_dir.split('.')[0]

        def get_all_config():
            configs = {}
            config_project_files = pipefunc.get_files(path=file_dir, file_type='*' + '.yml')

            for each_file in config_project_files:
                configs.update({each_file : self.get_config(each_file, file_dir, user_id)})
                
            return configs

        if not file_name: return get_all_config()

        file_name = file_name.split('.')[0].lower()
        file_path = os.path.normpath(f'{file_dir}/{file_name}.yml')

        # OPEN config path
        if os.path.exists(file_path):
            # self.LOG.debug(pipefunc.get_yaml_content(file_path, self.paths))
            return pipefunc.get_yaml_content(file_path, self.paths)
        else: 
            print(f"CAN'T find file: {file_path}")
        
        return ''


    def set_config(self, path, key, value):
        if os.path.exists(path):
            tmp_content = pipefunc.get_yaml_content(path, self.paths)
        else:
            tmp_content = {}
            pipefunc.create_folder(path)

        tmp_content[key] = value
        pipefunc.set_yaml_content(path, tmp_content)


    def get_img_path(self, end_path='btn/default'):
        img_format = '' if '.' in end_path else '.png'

        path = f'{self.paths["pipeline"]}/img/{end_path}{img_format}' or \
               f'{self.paths["pipeline"]}/img/{os.path.dirname(end_path)}/default{img_format}' or \
               f'{self.paths["pipeline"]}/img/btn/default{img_format}'

        return path


    #*********************************************************************
    # PIPELINE
    @property
    def paths(self):
        return eval(os.environ['PLEX_PATHS'])
    
    @property
    def context(self):
        return eval(os.environ['PLEX_CONTEXT'])

   
    #*********************************************************************
    # PROJECT    
    @property
    def project_names(self):
        projects_path = self.paths['config_projects']
        return [os.path.basename(f.path) for f in os.scandir(projects_path) if f.is_dir()]
    
    
    #*********************************************************************
    # USER  
    @property
    def user_id(self):
        return getpass.getuser()
    
    @property
    def admin(self):
        return eval(os.environ['PLEX_CONTEXT'])['admin']
   
    @property    
    def user_sandbox(self):
        user_sandbox_path = f'{self.config_project["PATH"]["sandbox"]}/{self.user_id}'
        if not os.path.exists(user_sandbox_path): pipefunc.create_folder(user_sandbox_path)
        return user_sandbox_path
    

    #*********************************************************************
    # BUTTON
    def report(self):
        self.help('report')

    def help(self, name=''):
        name = name or Tank().software_name
        webbrowser.open(self.config_project['URL'].get(name, self.config_project['URL']['default']))