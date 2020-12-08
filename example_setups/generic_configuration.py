
class generic_configuration:

    def __init__(self,cfg_name = "Unnamed Configuration"):
        self.config_list = list()
        self.name = cfg_name
        self.path = "defaultPath"

    def set_path(self,new_path):
        self.path = new_path

    def get_filename(self, index):
        """ Overload function to create custom filenames """
        return self.config_list[index].get_filename()

    def get_path(self):
        return self.path

    def __iter__(self):
        return self.config_list.__iter__()

    def print_configuration(self):
        ret = "Configuration \"{}\" is :\n".format(self.name)
        i = 0
        for c in self.config_list:
            ret += "Configuration {:3}: [{}]\n".format(i, c)
            i += 1
        return ret