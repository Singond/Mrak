from log import logger
from vyper import v

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
        logger.debug("Reading configuration from %s", v.config_file_used())
        v.read_in_config()

        self.remotes = []
        for remoteconfig in v.get("remotes"):
            remote = Remote(remoteconfig)
            self.remotes.append(remote)
            logger.debug("Configured remote %s", remote)

    def display_config(self):
        print("Configured remotes:")
        for remote in self.remotes:
            print(remote)

class Remote:
    '''
    Configuration for an rclone remote.
    '''

    def __init__(self, config):
        self.name = config["name"]
        if "label" in config:
            self.label = config["label"]
        else:
            self.label = self.name
        self.localdir = config["dir"]

    def __str__(self):
        return f"{self.name} -> {self.localdir}"
