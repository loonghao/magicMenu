# Import built-in modules.
import os
import sys

# Import third-party modules.
import yaml


def load_yaml(yaml_file):
    """Load yaml file."""
    with open(yaml_file, 'r') as yaml_obj:
        data = yaml.load(yaml_obj)
    return data


def path_join(path, *paths):
    """Join two (or more) paths."""
    return os.path.join(path, *paths).replace('\\', '/')


def touch(filename):
    """As unix system touch, create a file if it does not exist,
     and update is mtime if it does.

    Args:
        filename (str): path to the file to be updated.
    
    """
    try:
        os.utime(filename, None)
    except OSError:
        open(filename, 'a').close()


def create_missing_directories(dir_):
    """Create missing directories if the directory does not already exist.

    Args:
        dir_ (str): directory that will be created
         if it does not already exist.
    """

    if not os.path.isdir(dir_):
        os.makedirs(dir_)


class BaseMenu(object):
    def __init__(self):
        self.config_data = load_yaml(
            path_join(os.path.dirname(__file__), 'config.yaml'))
        self.user_shelf_root = self.config_data['root'].get('user')
        self.project_shelf_root = self.config_data['root'].get('project')
        self.user_shelf_path = path_join(self.user_shelf_root, '.magicMenu')
        if not os.path.exists(self.user_shelf_path):
            create_missing_directories(self.user_shelf_path)

    def find_project_override(self):
        pass

    def get_user_shelf(self, run_mode):
        user_shelf = path_join(self.user_shelf_path, run_mode)
        if not os.path.exists(user_shelf):
            create_missing_directories(user_shelf)
        return path_join(self.user_shelf_path, run_mode)

    def add_user_menu(self):
        pass

    def open_user_menu_folder(self):
        pass

    def open_project_menu_folder(self):
        pass

    def get_project_shelf(self, project, run_mode):
        project_shelf = path_join(self.project_shelf_root, project, '_common',
                                  'magicMenu', run_mode)
        if not os.path.exists(project_shelf):
            create_missing_directories(project_shelf)
        return path_join(self.project_shelf_root, project, '_common',
                         'magicMenu', run_mode)

    @staticmethod
    def order_button(global_shelf, shelf_name):
        btns = global_shelf['shelves'][shelf_name]
        for btn in btns:
            btns[btn]['order'] = btns[btn].get('order', 10)
        if btns:
            return sorted(btns, key=lambda key: btns[key]['order'])
        else:
            return {}

    @staticmethod
    def load_script(module):
        if module:
            if os.path.isfile(module):
                module = os.path.dirname(module)
            if module not in sys.path:
                sys.path.append(module)
            if os.path.exists(module) and not module.endswith('mel'):
                touch(path_join(module, '__init__.py'))
