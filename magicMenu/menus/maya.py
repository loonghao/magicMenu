import glob
import logging
import os
import re
import sys

import maya.mel
import pymel.core as pm

from .base import BaseMenu


class MayaShelve(BaseMenu):
    def __init__(self):
        global MAIN_MENU
        global PROJECT_MAIN_MENU
        super(MayaShelve, self).__init__()
        self.project_name = None
        user_e = False
        project_e = False
        profile = os.getenv('MAYA_PROFILE_PATH')
        m = re.match('(.+)projects.(?P<project>[a-z]+_[a-zA-Z0-9]{3}-[0-9]+).+', profile)
        user_object = pft.get_user_name().replace('.', '_')
        for a in pm.lsUI(m=True, l=True):
            if a.find('|{0}'.format(user_object)) != -1:
                user_e = True
        if not user_e:
            MAIN_MENU = pm.menu(pft.get_user_name(), label=pft.get_user_name(), parent='MayaWindow', tearOff=True)
        if m:
            self.project_name = m.groupdict()['project']
            self.project = self.project_name.split('-')[0].split('_')[1]
            for a in pm.lsUI(m=True, l=True):
                if a.find('|{0}'.format(self.project)) != -1:
                    project_e = True
            if not project_e:
                PROJECT_MAIN_MENU = pm.menu(self.project, label=self.project, parent='MayaWindow', tearOff=True)

    def find_project_override(self):
        scene_name = pm.sceneName()
        try:
            details = pft.PathDetails.parse_path(scene_name)
        except RuntimeError:
            logging.warning("Can not parse this file path, lets go with the default shelves")
            return {}
        project_name = details.get_project_path_name()
        if sys.platform == "win32" and not details.root.endswith("\\"):
            details.root += "\\"
        shelf_override = pft.pathjoin(details.root, project_name, "config", "shelf_override.yaml")
        if os.path.exists(shelf_override):
            print "project override file exists %s" % shelf_override
            try:
                project_shelf_file = pft.load_yaml(shelf_override)
                return project_shelf_file['shelves']
            except Exception, error:
                print "failed to parse %s " % shelf_override
                print error

        return {}

    @staticmethod
    def get_localized_global_shelf():
        default_shelf_name = 'maya_shelves.yaml'
        global_shelf_path = pft.pathjoin(pft.pathjoin(pixoConfig.CONFIG_DIR, default_shelf_name))
        print global_shelf_path
        return global_shelf_path

    def load_shelves(self):
        pixoConfig.Logging.configure()
        global_shelf_name = self.get_localized_global_shelf()
        global_shelf = pft.load_yaml(global_shelf_name)
        global_shelf['shelves'].update()
        overrides = self.find_project_override()
        for okey in overrides:
            if okey in global_shelf['shelves']:
                global_shelf['shelves'][okey].update(overrides[okey])
            else:
                global_shelf['shelves'][okey] = overrides[okey]

        parent = self.top_shelf()
        shelf_dict = global_shelf['shelves']

        for shelf_name in shelf_dict.keys():
            self.delete_shelf(parent, shelf_name)
            shelf = self.create_shelf(parent, shelf_name)
            sdict = global_shelf['shelves'][shelf_name]
            for button in self.order_button(global_shelf, shelf_name):
                icon = "pythonFamily.xpm"
                command = ""
                if 'icon' in sdict[button]:
                    icon = sdict[button]['icon']
                    if icon.startswith("./"):
                        icon = icon.replace("./", pft.pathjoin(pixoConfig.UI_DIR, "elements/"))
                if 'command' in sdict[button] and sdict[button]['command']:
                    command = sdict[button]['command']
                print "adding button %s " % button

                pm.shelfButton(label=button, parent=shelf, command=command, image1=icon)

    @staticmethod
    def top_shelf():
        top_shelf_name = maya.mel.eval('$tmpVar=$gShelfTopLevel')
        shelf_tab = pm.tabLayout(top_shelf_name, query=True, fullPathName=True)
        return shelf_tab

    @staticmethod
    def find_shelf_by_name(parent, shelf_name):
        shelf_exists = pm.shelfLayout(shelf_name, exists=True, parent=parent)
        shelf = None
        if shelf_exists:
            shelf = pm.shelfLayout(shelf_name,
                                   query=True,
                                   fullPathName=True)
        return shelf

    def delete_shelf(self, parent, shelf_name):
        shelf = self.find_shelf_by_name(parent, shelf_name)
        if shelf:
            pm.deleteUI(shelf)

    @staticmethod
    def create_shelf(parent, shelf_name):
        shelf = pm.shelfLayout(shelf_name, parent=parent)
        return shelf

    def open_user_menu_folder(self):
        pft.start(self.get_user_shelf('maya'))

    def open_project_menu_folder(self):
        pft.start(self.get_project_shelf(self.project_name, 'maya'))

    def add_user_menu(self):
        user_object = pft.get_user_name().replace('.', '_')
        for a in pm.lsUI(m=True, l=True):
            if a.find('|{0}|'.format(user_object)) != -1:
                pm.deleteUI(a)
        for a in pm.lsUI(mi=True, l=True):
            if a.find('|{0}|user_reload_menu'.format(user_object)) != -1:
                pm.deleteUI(a)
        pm.menuItem('user_reload_menu', label='reload_menu',
                    command="import pixoShelves.shelves.Maya as maya_shelf;reload(maya_shelf);"
                            "dd = maya_shelf.MayaShelve();"
                            "dd.add_user_menu();",
                    parent=MAIN_MENU)
        for a in pm.lsUI(mi=True, l=True):
            if a.find('|{0}|user_open_menu_folder'.format(user_object)) != -1:
                pm.deleteUI(a)
        pm.menuItem('user_open_menu_folder', label='open_menu_folder',
                    command="import pixoShelves.shelves.Maya as maya_shelf;reload(maya_shelf);"
                            "dd = maya_shelf.MayaShelve();"
                            "dd.open_user_menu_folder();",
                    parent=MAIN_MENU)
        for a in pm.lsUI(mi=True, l=True):
            if a.find('|{0}|user_divider'.format(user_object)) != -1:
                pm.deleteUI(a)
        pm.menuItem('user_divider', divider=True, parent=MAIN_MENU)
        files = []
        folder_shelf = []
        menu_folder = self.get_user_shelf('maya')
        for m in os.listdir(menu_folder):
            files.extend(glob.glob(pft.pathjoin(menu_folder, '*.pixoshelf')))
            sub_folder = pft.pathjoin(menu_folder, m)
            if os.path.isdir(sub_folder):
                print sub_folder
                folder_shelf.extend(glob.glob(pft.pathjoin(pft.pathjoin(menu_folder, m), '*.pixoshelf')))
        pixoshelfs = [f.replace('\\', '/') for f in files]
        pixo_folder_shelf = [f.replace('\\', '/') for f in folder_shelf]

        for f in pixo_folder_shelf:
            sub_menu_name = os.path.dirname(f).split('/')[-1]
            sub_menu = pm.menuItem(sub_menu_name, subMenu=True, parent=MAIN_MENU)
            d = pft.load_yaml(f)
            command_line = d.get('python')
            if not command_line:
                command_line = d.get('mel')
                command = {'mel': command_line}
            else:
                command = {'python': command_line}
            script_name = os.path.basename(f).split('.pixoshelf')[0]
            script_path = d.get('script')
            if script_path:
                if script_path.startswith("./"):
                    script_path = script_path.replace("./", "{0}/".format(os.path.dirname(f)))
                if not script_path:
                    raise RuntimeError('not find script path')
                self.load_script(script_path)
            if command.keys()[0] == 'mel':
                pm.menuItem(label=script_name,
                            command='mel.eval("""source "{0}";{1}""")'.format(script_path, command['mel']),
                            parent=sub_menu)
            else:
                if script_path:
                    if script_path.endswith('mel'):
                        pm.menuItem(label=script_name,
                                    command='mel.eval("""source "{0}";""")'.format(script_path),
                                    parent=sub_menu)
                pm.menuItem(label=script_name, command='{0}'.format(command['python']), parent=sub_menu)

        for f in pixoshelfs:
            d = pft.load_yaml(f)
            command_line = d.get('python')
            if not command_line:
                command_line = d.get('mel')
                command = {'mel': command_line}
            else:
                command = {'python': command_line}
            script_name = os.path.basename(f).split('.pixoshelf')[0]
            script_path = d.get('script')
            if script_path:
                if script_path.startswith("./"):
                    script_path = script_path.replace("./", "{0}/".format(os.path.dirname(f)))
                if not script_path:
                    raise RuntimeError('not find script path')
                self.load_script(script_path)
            if command.keys()[0] == 'mel':
                pm.menuItem(label=script_name,
                            command='mel.eval("""source "{0}";{1}""")'.format(script_path, command['mel']),
                            parent=MAIN_MENU)
            else:
                if script_path:
                    if script_path.endswith('mel'):
                        pm.menuItem(label=script_name,
                                    command='mel.eval("""source "{0}";""")'.format(script_path),
                                    parent=MAIN_MENU)
                pm.menuItem(label=script_name, command='{0}'.format(command['python']), parent=MAIN_MENU)

    def add_project_menu(self):
        if self.project_name:
            for a in pm.lsUI(m=True, l=True):
                if a.find('|{0}|'.format(self.project)) != -1:
                    pm.deleteUI(a)
            for a in pm.lsUI(mi=True, l=True):
                if a.find('|{0}|project_reload_menu'.format(self.project)) != -1:
                    pm.deleteUI(a)
            pm.menuItem('project_reload_menu', label='reload_menu',
                        command="import pixoShelves.shelves.Maya as maya_shelf;reload(maya_shelf);"
                                "dd = maya_shelf.MayaShelve();"
                                "dd.add_project_menu();",
                        parent=PROJECT_MAIN_MENU)
            for a in pm.lsUI(mi=True, l=True):
                if a.find('|{0}|project_open_menu_folder'.format(self.project)) != -1:
                    pm.deleteUI(a)
            pm.menuItem('project_open_menu_folder', label='open_menu_folder',
                        command="import pixoShelves.shelves.Maya as maya_shelf;reload(maya_shelf);"
                                "dd = maya_shelf.MayaShelve();"
                                "dd.open_project_menu_folder();",
                        parent=PROJECT_MAIN_MENU)
            for a in pm.lsUI(mi=True, l=True):
                if a.find('|{0}|project_divider'.format(self.project)) != -1:
                    pm.deleteUI(a)
            pm.menuItem('project_divider', divider=True, parent=PROJECT_MAIN_MENU)
            files = []
            folder_shelf = []
            menu_folder = self.get_project_shelf(self.project_name, 'maya')
            for m in os.listdir(menu_folder):
                files.extend(glob.glob(pft.pathjoin(menu_folder, '*.pixoshelf')))
                sub_folder = pft.pathjoin(menu_folder, m)
                if os.path.isdir(sub_folder):
                    print sub_folder
                    folder_shelf.extend(glob.glob(pft.pathjoin(pft.pathjoin(menu_folder, m), '*.pixoshelf')))
            pixoshelfs = [f.replace('\\', '/') for f in files]
            pixo_folder_shelf = [f.replace('\\', '/') for f in folder_shelf]

            for f in pixo_folder_shelf:
                sub_menu_name = os.path.dirname(f).split('/')[-1]
                sub_menu = pm.menuItem(sub_menu_name, subMenu=True, parent=PROJECT_MAIN_MENU)
                d = pft.load_yaml(f)
                command_line = d.get('python')
                if not command_line:
                    command_line = d.get('mel')
                    command = {'mel': command_line}
                else:
                    command = {'python': command_line}
                script_name = os.path.basename(f).split('.pixoshelf')[0]
                script_path = d.get('script')
                if script_path:
                    if script_path.startswith("./"):
                        script_path = script_path.replace("./", "{0}/".format(os.path.dirname(f)))
                    if not script_path:
                        raise RuntimeError('not find script path')
                    self.load_script(script_path)
                if command.keys()[0] == 'mel':
                    pm.menuItem(label=script_name,
                                command='mel.eval("""source "{0}";{1}""")'.format(script_path, command['mel']),
                                parent=sub_menu)
                else:
                    if script_path:
                        if script_path.endswith('mel'):
                            pm.menuItem(label=script_name,
                                        command='mel.eval("""source "{0}";""")'.format(script_path),
                                        parent=PROJECT_MAIN_MENU)
                    pm.menuItem(label=script_name, command='{0}'.format(command['python']), parent=sub_menu)

            for f in pixoshelfs:
                d = pft.load_yaml(f)
                command_line = d.get('python')
                if not command_line:
                    command_line = d.get('mel')
                    command = {'mel': command_line}
                else:
                    command = {'python': command_line}
                script_name = os.path.basename(f).split('.pixoshelf')[0]
                script_path = d.get('script')
                if script_path:
                    if script_path.startswith("./"):
                        script_path = script_path.replace("./", "{0}/".format(os.path.dirname(f)))
                    if not script_path:
                        raise RuntimeError('not find script path')
                    self.load_script(script_path)
                if command.keys()[0] == 'mel':
                    pm.menuItem(label=script_name,
                                command='mel.eval("""source "{0}";{1}""")'.format(script_path, command['mel']),
                                parent=PROJECT_MAIN_MENU)
                else:
                    if script_path:
                        if script_path.endswith('mel'):
                            pm.menuItem(label=script_name,
                                        command='mel.eval("""source "{0}";""")'.format(script_path),
                                        parent=PROJECT_MAIN_MENU)
                    pm.menuItem(label=script_name, command='{0}'.format(command['python']),
                                parent=PROJECT_MAIN_MENU)
