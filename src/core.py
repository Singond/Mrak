import os
from log import logger
from vyper import v


class Mrak:
    """
    An instance of the Mrak application.
    """

    def __init__(self, configfile=None):
        """
        Create a new instance with the given configuration file.
        If the configuration file is omitted, search for a file called
        ~/.config/mrak/config.*`.
        """
        if configfile is None:
            v.set_config_name("config")
            v.add_config_path("$HOME/.config/mrak")
        else:
            v.set_config_file(configfile)
        logger.debug("Reading configuration from %s", v.config_file_used())
        v.read_in_config()
        v.set_default("rclone_executable", "rclone")

        self.configure(v)

    def configure(self, v):
        """Configure Mrak from the given vyper configuration object."""
        self.remotes = []
        for remoteconfig in v.get("remotes"):
            remote = Remote(remoteconfig)
            self.remotes.append(remote)
            logger.debug("Configured remote %s", remote)

    def display_config(self):
        print("Configured remotes:")
        for remote in self.remotes:
            print(remote)

    def _rclone(self, args):
        rclone = v.get("rclone_executable")
        cmd = f"{rclone} {args}"
        logger.debug("Running command: %s", cmd)
        os.system(cmd)

    def update_local(self, remote):
        """
        Update the local directory with files from the remote.
        """
        self._rclone((
            f"--dry-run copy --update "
            f"{remote.full_remotepath()} {remote.localpath}"))


class Remote:
    """
    Configuration for an rclone remote.
    """

    def __init__(self, config):
        self.remotepath = config["remotepath"]
        self.localpath = config["localpath"]
        if "label" in config:
            self.label = config["label"]
        else:
            self.label = self.name

    def full_remotepath(self):
        if ":" in self.remotepath:
            return self.remotepath
        else:
            return self.remotepath + ":"

    def __str__(self):
        return f"{self.remotepath} -> {self.localpath}"
