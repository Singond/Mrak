Running
=======
Installing PyGObject may require Gobject development package.
On Debian-based distributions, install `libgirepository1.0-dev`,
on Arch, install `gobject-introspection`. (For details, see
<https://stackoverflow.com/questions/18025730/pygobject-2-28-6-wont-configure-no-package-gobject-introspection-1-0-found>).

To run the application, execute the following command in the project root:
```bash
poetry run mrak --config-file=<path-to-config-file>
```
The --config-file parameter can be omitted if there is a `config.yaml`
or `config.toml` file in the `~/.config/mrak` directory.
