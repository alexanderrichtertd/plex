# content   = main hub
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys
import getpass
import webbrowser

import plexfunc


class Plex(plexfunc.Singleton):

    # SOFTWARE ************************************************************
    @property
    def software(self):
        """ Get the current software object based on the environment variable.
            RETURN: software class e.g. maya_dcc.Maya()
        """
        module_name = f"{self.software_name}_dcc" if self.software_name else 'software'
        class_name = self.software_name.title() or 'Software'

        try:
            module = __import__(module_name, fromlist=[class_name])
            return getattr(module, class_name)()
        except ImportError:
            from software import Software
            return Software()

    @property
    def software_name(self):
        return self.context['software']

    @property
    def log(self):
        import plexlog
        return plexlog.init
   
    @property
    def announcement(self):
        # announcement order: overwrite than plex or project 
        return self.config['plex']['announcement'] if self.config['plex']['announcement'] else self.config['project']['announcement']
    

    # CONFIG *************************************************************
    @property
    def config(self):
        """Merge all config files into one dictionary
            RETURN: dict of all config files
        """
        if 'PLEX_CONFIG' not in os.environ:
            return self.config_refresh()
        all_config = eval(os.environ['PLEX_CONFIG'])

        if all_config.get('software_name') != self.software_name:
            all_config['software'] = self.config_software
            all_config['software_name'] = self.software_name
            os.environ['PLEX_CONFIG'] = str(all_config)

        return all_config

    def config_refresh(self):
        all_config = {
            'plex':     self.get_config('plex'),
            'project':  self.get_config('project'),
            'script':   self.get_config('script'),
            'meta':     self.get_config('meta'),
            'software': self.config_software if self.software_name else {},
            'software_name': self.software_name
        }
        os.environ['PLEX_CONFIG'] = str(all_config)
        return all_config
    
    @property
    def config_software(self):
        return self.get_config(f'software/{self.software_name}')


    # CONFIG: Get & Set **************************************************
    def get_config(self, file_name='', file_dir=''):
        if not file_dir:
            file_dir = self.get_config_path(file_name)

        # Handle file name and extension
        base_name = os.path.splitext(file_name)[0]
        file_path = os.path.normpath(os.path.join(file_dir, f"{base_name}.yml"))
        
        if os.path.exists(file_path):
            return plexfunc.get_yaml_content(file_path, (self.paths | self.context))
        
        print(f"CAN'T find file: {file_path}")
        return {}


    def set_config(self, path, key, value):
        if os.path.exists(path):
            tmp_content = plexfunc.get_yaml_content(path, self.paths)
        else:
            tmp_content = {}
            plexfunc.create_dir(path)

        tmp_content[key] = value
        plexfunc.set_yaml_content(path, tmp_content)


    def get_config_path(self, file_name=''):
        """Get the correct config directory path without file extension"""
        if file_name == 'plex':
            file_dir = self.paths['config']
        elif file_name == 'user':
            file_dir = self.paths['config_user']
        else:
            file_dir = self.paths['config_project']

        # Remove .yml if it exists in file_name
        file_name = os.path.splitext(file_name)[0]
        return os.path.normpath(file_dir)


    def get_img_path(self, end_path='btn/default'):
        img_format = '' if '.' in end_path else '.png'

        path = f'{self.paths["plex"]}/img/{end_path}{img_format}' or \
               f'{self.paths["plex"]}/img/{os.path.dirname(end_path)}/default{img_format}' or \
               f'{self.paths["plex"]}/img/btn/default{img_format}'

        return path


    # PLEX ***************************************************************
    @property
    def paths(self):
        return eval(os.environ['PLEX_PATHS'])
    
    @property
    def context(self):
        return eval(os.environ['PLEX_CONTEXT'])
    
    def set_context(self, key, value):
        context = eval(os.environ['PLEX_CONTEXT'])
        context[key] = value
        os.environ['PLEX_CONTEXT'] = str(context)


    # PROJECT ************************************************************    
    @property
    def project_names(self):
        projects_path = self.paths['config_projects']
        return [os.path.basename(f.path) for f in os.scandir(projects_path) if f.is_dir()]
    
    
    # USER ***************************************************************  
    @property
    def user_id(self):
        return getpass.getuser()
    
    @property
    def admin(self):
        return eval(os.environ['PLEX_CONTEXT'])['admin']
   
    @property    
    def user_sandbox(self):
        user_sandbox_path = f'{self.config["project"]["PATH"]["sandbox"]}/{self.user_id}'
        plexfunc.create_dir(user_sandbox_path)
        return user_sandbox_path


    # BUTTON **************************************************************
    def help(self, name=''):
        name = name or self.software_name
        webbrowser.open(self.config['project']['URL'].get(name, self.config['project']['URL']['default']))


# Redirect module to singleton instance
sys.modules[__name__] = Plex()