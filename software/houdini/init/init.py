# content   = houdini init
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

from plex import Plex

LOG = Plex().log(script=__name__)


def add_menu():
    menu_path = f'{Plex().paths["software"]}/houdini/scripts/MainMenuMaster.xml'

    def find_inbetween(self, text, first, last):
        try:
            return text.split(first, 1)[1].split(last, 1)[0]
        except (IndexError, ValueError):
            return ""

    try:
        with open(menu_path, 'r+') as outfile:
            content = outfile.read()
            find_title = find_inbetween(content, '<label>', '</label>')
            content = content.replace(f'<label>{find_title}</label>', f'<label>{Plex().context["project_name"]}</label>')
            print(content)
            # WRITE new XML
            outfile.seek(0)
            outfile.write(content)
            outfile.truncate()
    except: LOG.error(f'FILE not found: {menu_path}', exc_info=True)
