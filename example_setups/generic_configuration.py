
class generic_configuration:

    def __init__(self):
        self.config_list = list()

    def __iter__(self):
        return self.config_list.__iter__()

    def print_configuration(self):
        ret = ""
        i = 0
        for c in self.config_list:
            cfg = "(A:{}, F:{})".format(c.amplitude,c.frequency)
            ret += "Configuration {:3}: [{}]\n".format(i, cfg)
            i += 1
        return ret