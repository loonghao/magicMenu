import glob
import os
import sys

import nuke

import yaml
from .base import BaseMenu


class NukeShelves(BaseMenu):
    def __init__(self):
        super(NukeShelves, self).__init__()
        self.project_name = os.getenv('projectNameLong')
        self.root_menu = nuke.menu("Nuke")
        self.user_object = pft.get_user_name()
        self.user_menu = self.root_menu.addMenu(self.user_object)
        self.project = self.project_name.split('-')[0].split('_')[1]
        self.project_menu = self.root_menu.addMenu(self.project)
        root_menu_nodes = nuke.menu('Nodes')
        self.root_menu_nodes = root_menu_nodes.addMenu('pixoShelvesNodes')

    def add_plugins(self, project_path=None):
        nuke.pluginAddPath(pft.pathjoin(pixoConfig.LIBS_DIR, 'ui/elements').replace('\\', '/'))
        if project_path:
            shelf_path = project_path
            nuke.pluginAddPath(project_path)
            nuke.pluginAddPath('%s/nuke_gizmos' % shelf_path)
            nuke.pluginAddPath('%s/nuke_python' % shelf_path)
            nuke.pluginAddPath('%s/nuke_scripts' % shelf_path)
            nuke.pluginAddPath('%s/nuke_tcl' % shelf_path)
            nuke.pluginAddPath('%s/nuke_plugins' % shelf_path)
        else:
            shelf_path = pft.pathjoin(pixoConfig.APP_PATH, 'pixoNuke/shelf').replace('\\', '/')
            nuke.pluginAddPath('%s/nuke_gizmos' % shelf_path)
            nuke.pluginAddPath('%s/nuke_python' % shelf_path)
            nuke.pluginAddPath('%s/nuke_scripts' % shelf_path)
            nuke.pluginAddPath('%s/nuke_tcl' % shelf_path)
            nuke.pluginAddPath('%s/nuke_plugins' % shelf_path)

    def find_project_override(self):
        # this will never work in SHX
        if pft.get_short_name() == 'pek':
            root = pixoConfig.PixoConfig.get_path('asset_root')
            if sys.platform == "win32" and not root.endswith("\\"):
                root += "\\"
            shelf_override = pft.pathjoin(root, self.project_name, "config", "nuke_shelf_override.yaml")
            project_tools_dir = pft.pathjoin(root, self.project_name, "config/nuke")
            if os.path.exists(project_tools_dir):
                self.add_plugins(pft.pathjoin(root, self.project_name, "config/nuke"))
            if os.path.exists(shelf_override):
                print "project override file exists %s" % shelf_override
                try:
                    project_shelf_file = yaml.load(file(shelf_override))
                    return project_shelf_file['shelves']
                except Exception, error:
                    print "failed to parse %s " % shelf_override
                    print error
        else:
            return {}

    @staticmethod
    def sort_data(global_shelf, shelf_name):
        btns = global_shelf['shelves'][shelf_name]
        for btn in btns:
            btns[btn]['order'] = btns[btn].get('order', 10)
            btns[btn]['icon'] = btns[btn].get('icon', '')
            btns[btn]['shortcutkey'] = btns[btn].get('shortcutkey', '')
        if btns:
            return sorted(btns, key=lambda key: btns[key]['order'])
        else:
            return {}

    def load_shelves(self):
        if nuke.env['gui']:
            pixoConfig.Logging.configure()
            self.add_plugins()
            global_shelf_path = pft.pathjoin(
                pft.pathjoin(pft.pathjoin(pixoConfig.APP_PATH, 'config'), 'nuke_shelves.yaml'))
            global_shelf = yaml.load(file(global_shelf_path))
            global_shelf['shelves'].update()

            overrides = self.find_project_override()
            if overrides:
                for okey in overrides:
                    if okey in global_shelf['shelves']:
                        global_shelf['shelves'][okey].update(overrides[okey])
                    else:
                        global_shelf['shelves'][okey] = overrides[okey]

            shelf_dict = global_shelf['shelves']
            toolbar = nuke.menu("Nodes")
            t = toolbar.addMenu("PixoPipe", icon="nuke_pixo.png")
            for shelf_name in shelf_dict.keys():
                new_menu = t.addMenu(shelf_name)
                for button in self.sort_data(global_shelf, shelf_name):
                    command = shelf_dict[shelf_name][button]
                    icon = command['icon']
                    shortcutkey = command['shortcutkey']
                    new_menu.addCommand(button, "%s" % command['command'], shortcutkey, icon=icon)

    def open_user_menu_folder(self):
        pft.start(self.get_user_shelf('nuke'))

    def open_project_menu_folder(self):
        pft.start(self.get_project_shelf(self.project_name, 'nuke'))

    def add_user_menu(self):
        files = []
        folder_shelf = []
        menu_folder = self.get_user_shelf('nuke')
        self.user_menu.addCommand('Reload Menu', "import pixoShelves.shelves.Nuke as nuke_shelf;reload(nuke_shelf);"
                                                 "dd = nuke_shelf.NukeShelves();"
                                                 "dd.add_user_menu();", icon='NukeGear.png')
        self.user_menu.addCommand('Open Menu Folder',
                                  "import pixoShelves.shelves.Nuke as nuke_shelf;reload(nuke_shelf);"
                                  "dd = nuke_shelf.NukeShelves();"
                                  "dd.open_user_menu_folder();", icon='NukeGear.png')

        self.user_menu.addCommand('-', "")

        for m in os.listdir(menu_folder):
            if m == 'ToolSets':
                tool_sets = self.root_menu_nodes
                tool_sets.removeItem(self.user_object)
                user_tool_sets = tool_sets.addMenu(self.user_object)
                tool_sets_root = pft.pathjoin(menu_folder, m)
                for s in os.listdir(tool_sets_root):
                    file_ = pft.pathjoin(tool_sets_root, s)
                    if os.path.isfile(file_):
                        if s.endswith('nk'):
                            name_ = s.split('.nk')[0]
                            user_tool_sets.addCommand(name_, 'nuke.loadToolset("{0}")'.format(file_))
                        if s.endswith('gizmo'):
                            name_ = s.split('.gizmo')[0]
                            file_ = pft.pathjoin(tool_sets_root, s)
                            user_tool_sets.addCommand(name_, 'nuke.loadToolset("{0}")'.format(file_))
                    else:
                        for sub_d in os.listdir(file_):
                            sub_file = pft.pathjoin(file_, sub_d)
                            if sub_d.endswith('nk'):
                                sub_folder_name = s.split('.nk')[0]
                                name_ = sub_d.split('.nk')[0]
                                user_tool_sets.addCommand('{0}/{1}'.format(sub_folder_name, name_),
                                                          'nuke.loadToolset("{0}")'.format(sub_file))
                            if sub_d.endswith('gizmo'):
                                sub_folder_name = s.split('.gizmo')[0]
                                name_ = sub_d.split('.gizmo')[0]
                                file_ = pft.pathjoin(tool_sets_root, s)
                                user_tool_sets.addCommand('{0}/{1}'.format(sub_folder_name, name_),
                                                          'nuke.loadToolset("{0}")'.format(sub_file))
            else:
                files = glob.glob(pft.pathjoin(menu_folder, '*.pixoshelf'))
                sub_folder = pft.pathjoin(menu_folder, m)
                if os.path.isdir(sub_folder):
                    folder_shelf = glob.glob(pft.pathjoin(pft.pathjoin(menu_folder, m), '*.pixoshelf'))
        pixoshelfs = [f.replace('\\', '/') for f in files]
        pixo_folder_shelf = [f.replace('\\', '/') for f in folder_shelf]
        self.user_menu.addCommand('-', "")
        for f in pixo_folder_shelf:
            sub_menu_name = os.path.dirname(f).split('/')[-1]
            self.user_menu.removeItem(sub_menu_name)
            sub_menu = self.user_menu.addMenu(sub_menu_name)
            d = pft.load_yaml(f)
            script_name = os.path.basename(f).split('.pixoshelf')[0]
            if not script_name:
                raise RuntimeError('script name')
            script_path = d.get('script')
            if script_path:
                if script_path.startswith("./"):
                    script_path = script_path.replace("./", "{0}/".format(os.path.dirname(f)))
                if not script_path:
                    raise RuntimeError('not find script path')
                self.load_script(script_path)
            command_line = d.get('python')
            if not command_line:
                command_line = d.get('nukescript')
                command = {'nukescript': command_line}
            else:
                command = {'python': command_line}
            if not command_line:
                raise RuntimeError('not find command')

            if command.keys()[0] == 'nukescript':
                nuke_file = command['nukescript']
                if nuke_file.startswith("./"):
                    nuke_file = nuke_file.replace("./", "{0}/".format(os.path.dirname(f)))
                else:
                    nuke_file = nuke_file.replace('\\', '/')
                sub_menu.addCommand(script_name, 'nuke.nodePaste("{0}")'.format(nuke_file))
            else:
                sub_menu.addCommand(script_name, '{0}'.format(command['python']))

        self.user_menu.addCommand('-', "")
        for f in pixoshelfs:
            d = pft.load_yaml(f)
            script_name = os.path.basename(f).split('.pixoshelf')[0]
            script_path = d.get('script')
            if script_path:
                if script_path.startswith("./"):
                    script_path = script_path.replace("./", "{0}/".format(os.path.dirname(f)))
                if not script_path:
                    raise RuntimeError('not find script path')
                self.load_script(script_path)
            command_line = d.get('python')
            if not command_line:
                command_line = d.get('nukescript')
                command = {'nukescript': command_line}
            else:
                command = {'python': command_line}
            if not command_line:
                raise RuntimeError('not find command')
            if command.keys()[0] == 'nukescript':
                nuke_file = command['nukescript']
                if nuke_file.startswith("./"):
                    nuke_file = nuke_file.replace("./", "{0}/".format(os.path.dirname(f)))
                else:
                    nuke_file = nuke_file.replace('\\', '/')
                self.user_menu.removeItem(script_name)
                self.user_menu.addCommand(script_name, 'nuke.nodePaste("{0}")'.format(nuke_file))
            else:
                self.user_menu.removeItem(script_name)
                self.user_menu.addCommand(script_name, '{0}'.format(command['python']))

    def add_project_menu(self):
        if self.project_name:
            files = []
            folder_shelf = []
            menu_folder = self.get_project_shelf(self.project_name, 'nuke')
            self.project_menu.addCommand('Reload Menu',
                                         "import pixoShelves.shelves.Nuke as nuke_shelf;reload(nuke_shelf);"
                                         "dd = nuke_shelf.NukeShelves();"
                                         "dd.add_project_menu();", icon='NukeGear.png')
            self.project_menu.addCommand('Open Menu Folder',
                                         "import pixoShelves.shelves.Nuke as nuke_shelf;reload(nuke_shelf);"
                                         "dd = nuke_shelf.NukeShelves();"
                                         "dd.open_project_menu_folder();", icon='NukeGear.png')
            self.project_menu.addCommand('-', "")
            for m in os.listdir(menu_folder):
                if m == 'ToolSets':
                    tool_sets = self.root_menu_nodes
                    tool_sets.removeItem(self.project)
                    project_tool_sets = tool_sets.addMenu(self.project)
                    tool_sets_root = pft.pathjoin(menu_folder, m)
                    for s in os.listdir(tool_sets_root):
                        file_ = pft.pathjoin(tool_sets_root, s)
                        if os.path.isfile(file_):
                            if s.endswith('nk'):
                                name_ = s.split('.nk')[0]
                                project_tool_sets.addCommand(name_, 'nuke.loadToolset("{0}")'.format(file_))
                            if s.endswith('gizmo'):
                                name_ = s.split('.gizmo')[0]
                                file_ = pft.pathjoin(tool_sets_root, s)
                                project_tool_sets.addCommand(name_, 'nuke.loadToolset("{0}")'.format(file_))
                        else:
                            for sub_d in os.listdir(file_):
                                sub_file = pft.pathjoin(file_, sub_d)
                                if sub_d.endswith('nk'):
                                    sub_folder_name = s.split('.nk')[0]
                                    name_ = sub_d.split('.nk')[0]
                                    project_tool_sets.addCommand('{0}/{1}'.format(sub_folder_name, name_),
                                                                 'nuke.loadToolset("{0}")'.format(sub_file))
                                if sub_d.endswith('gizmo'):
                                    sub_folder_name = s.split('.gizmo')[0]
                                    name_ = sub_d.split('.gizmo')[0]
                                    file_ = pft.pathjoin(tool_sets_root, s)
                                    project_tool_sets.addCommand('{0}/{1}'.format(sub_folder_name, name_),
                                                                 'nuke.loadToolset("{0}")'.format(sub_file))
                else:
                    files = glob.glob(pft.pathjoin(menu_folder, '*.pixoshelf'))
                    sub_folder = pft.pathjoin(menu_folder, m)
                    if os.path.isdir(sub_folder):
                        folder_shelf = glob.glob(pft.pathjoin(pft.pathjoin(menu_folder, m), '*.pixoshelf'))
            pixoshelfs = [f.replace('\\', '/') for f in files]
            pixo_folder_shelf = [f.replace('\\', '/') for f in folder_shelf]
            self.project_menu.addCommand('-', "")
            for f in pixo_folder_shelf:
                sub_menu_name = os.path.dirname(f).split('/')[-1]
                self.project_menu.removeItem(sub_menu_name)
                sub_menu = self.project_menu.addMenu(sub_menu_name)
                d = pft.load_yaml(f)
                script_name = os.path.basename(f).split('.pixoshelf')[0]
                script_path = d.get('script')
                if script_path:
                    if script_path.startswith("./"):
                        script_path = script_path.replace("./", "{0}/".format(os.path.dirname(f)))
                    self.load_script(script_path)
                command_line = d.get('python')
                if not command_line:
                    command_line = d.get('nukescript')
                    command = {'nukescript': command_line}
                else:
                    command = {'python': command_line}
                if not command_line:
                    raise RuntimeError('not find command')
                if command.keys()[0] == 'nukescript':
                    nuke_file = command['nukescript']
                    if nuke_file.startswith("./"):
                        nuke_file = nuke_file.replace("./", "{0}/".format(os.path.dirname(f)))
                    else:
                        nuke_file = nuke_file.replace('\\', '/')
                    sub_menu.addCommand(script_name, 'nuke.nodePaste("{0}")'.format(nuke_file))
                else:
                    sub_menu.addCommand(script_name, '{0}'.format(command['python']))

            self.project_menu.addCommand('-', "")
            for f in pixoshelfs:
                d = pft.load_yaml(f)
                script_name = os.path.basename(f).split('.pixoshelf')[0]
                script_path = d.get('script')
                if script_path:
                    if script_path.startswith("./"):
                        script_path = script_path.replace("./", "{0}/".format(os.path.dirname(f)))
                    self.load_script(script_path)
                command_line = d.get('python')
                if not command_line:
                    command_line = d.get('nukescript')
                    command = {'nukescript': command_line}
                else:
                    command = {'python': command_line}
                if not command_line:
                    raise RuntimeError('not find command')

                if command.keys()[0] == 'nukescript':
                    nuke_file = command['nukescript']
                    if nuke_file.startswith("./"):
                        nuke_file = nuke_file.replace("./", "{0}/".format(os.path.dirname(f)))
                    else:
                        nuke_file = nuke_file.replace('\\', '/')
                    self.project_menu.removeItem(script_name)
                    self.project_menu.addCommand(script_name, 'nuke.nodePaste("{0}")'.format(nuke_file))
                else:
                    self.project_menu.removeItem(script_name)
                    self.project_menu.addCommand(script_name, '{0}'.format(command['python']))
