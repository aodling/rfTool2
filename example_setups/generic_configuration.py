
class generic_configuration:

    def __init__(self,cfg_name = "Unnamed Configuration"):
        self.config_list = list()
        self.name = cfg_name
        self.path = "defaultPath"
        self.file_prefix = "Config"
        self.rbw = 100e3
        self.span = 6e9

    def get_span_MHz(self):
        return self.span / 1e6

    def set_span(self,span):
        self.span = span

    def set_prefix(self,prefix):
        self.file_prefix = prefix

    def set_path(self,new_path):
        self.path = new_path

    def set_rbw(self,rbw : int):
        self.rbw = rbw

    def get_filename(self, index):
        """ Overload function to create custom filenames """
        return "{}{}{}kHz".format(self.file_prefix,
                                  self.config_list[index].get_filename(),self.rbw/1e3)

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