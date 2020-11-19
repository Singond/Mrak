from vyper import v

'''

'''
class Mrak:
    '''
    An instance of the Mrak application.
    '''

    def __init__(self, configfile=None):
        '''
        Create a new instance with the given configuration file.
        If the configuration file is omitted, search for a file called
        ~/.config/mrak/config.*`.
        '''

        if configfile is None:
            v.set_config_name("config")
            v.add_config_path("$HOME/.config/mrak")
        else:
            v.set_config_file(configfile)
        v.read_in_config()

    def foo(self):
        print(v.get("one"))
        print(v.get("two"))
        print(v.get("three"))