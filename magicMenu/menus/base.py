import os
import sys

import pixoFileTools as pft


class BaseMenu(object):
    def __init__(self):
        self.config_data = pft.load_yaml(pft.pathjoin(os.path.dirname(__file__), 'config.yaml'))
        self.user_shelf_root = self.config_data['root'].get('user')
        self.project_shelf_root = self.config_data['root'].get('project')
        self.user_shelf_path = pft.pathjoin(self.user_shelf_root, '.magicMenu')
        if not os.path.exists(self.user_shelf_path):
            pft.create_missing_directories(self.user_shelf_path)

    def find_project_override(self):
        pass

    def get_user_shelf(self, run_mode):
        user_shelf = pft.pathjoin(self.user_shelf_path, run_mode)
        if not os.path.exists(user_shelf):
            pft.create_missing_directories(user_shelf)
        return pft.pathjoin(self.user_shelf_path, run_mode)

    def add_user_menu(self):
        pass

    def open_user_menu_folder(self):
        pass

    def open_project_menu_folder(self):
        pass

    def get_project_shelf(self, project, run_mode):
        project_shelf = pft.pathjoin(self.project_shelf_root, project, '_common', 'magicMenu', run_mode)
        if not os.path.exists(project_shelf):
            pft.create_missing_directories(project_shelf)
        return pft.pathjoin(self.project_shelf_root, project, '_common', 'magicMenu', run_mode)

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
                pft.touch(pft.pathjoin(module, '__init__.py'))
