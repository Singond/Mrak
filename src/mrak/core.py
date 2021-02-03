import subprocess
import sys
from threading import Thread;
from tendo import singleton
import vyper; v = vyper.v
from mrak.log import logger


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

        # Check that the script is not running already
        try:
            self.lock = singleton.SingleInstance()
        except singleton.SingleInstanceException:
            print("Mrak is already running", file=sys.stderr)
            sys.exit(3)

        if configfile is None:
            v.set_config_name("config")
            v.add_config_path("$HOME/.config/mrak")
        else:
            v.set_config_file(configfile)

        try:
            v.read_in_config()
            logger.debug("Read configuration from file '%s'", v.config_file_used())
        except vyper.errors.UnsupportedConfigError:
            if not v.config_file_used():
                raise ConfigNotFoundException from None

        v.set_default("rclone_executable", "rclone")
        self.configure(v)

        self.rclonethread = None

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

    def _rclone(self, args, callback=None):
        """
        Run rclone with the giver arguments in a dedicated thread.
        Return the thread object.
        """
        thr = RcloneThread(args, callback)
        thr.start()
        return thr

    def update_local(self, remote, callback=None):
        """
        Update the local directory with files from the remote.
        """
        self.rclonethread = self._rclone(
            ["--dry-run", "copy", "--update",
             remote.full_remotepath(), remote.localpath],
            callback)

    def stop_rclone(self):
        if self.rclonethread and self.rclonethread.is_alive():
            self.rclonethread.stop()
        else:
            logger.warning("No living rclone process to terminate.")


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


class RcloneThread(Thread):
    """A thread with rclone process."""

    def __init__(self, rclone_args, callback, **kwargs):
        super().__init__(**kwargs)
        self.args = rclone_args
        self.callback = callback
        rclonecmd = v.get("rclone_executable")
        logger.debug("Running %s with arguments: %s", rclonecmd, rclone_args)
        self.proc = subprocess.Popen([rclonecmd, *rclone_args])

    def run(self):
        logger.info("Running rclone...")
        exitcode = self.proc.wait()
        logger.info("Rclone exited with code %d.", exitcode)
        self.callback()

    def stop(self):
        """Terminates the rclone process."""
        logger.info("Stopping rclone...")
        self.proc.terminate()
        logger.debug("Sent SIGTERM to rclone.")

class ConfigNotFoundException(Exception):
    pass