"""
A system tray interface for Mrak.
"""

import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Notify, AppIndicator3 as AppIndicator


def menu(mrak):
    """
    Create the menu for the system tray icon.
    """

    menu = Gtk.Menu()
    Notify.init("Mrak")

    for remote in mrak.remotes:
        item = Gtk.MenuItem(label=remote.label)
        item.set_submenu(submenu(mrak, remote))
        menu.append(item)

    menu.append(Gtk.SeparatorMenuItem())
    quitcmd = Gtk.MenuItem(label="Quit Mrak")
    quitcmd.connect("activate", close)
    menu.append(quitcmd)

    menu.show_all()
    return menu


def submenu(mrak, remote):
    submenu = Gtk.Menu()

    item = Gtk.MenuItem(label="Update local directory")
    item.connect("activate", lambda _: mrak.update_local(remote))
    submenu.append(item)

    return submenu


def close(_):
    """
    Remove Mrak system tray indicator.
    """
    Gtk.main_quit()


def run(app):
    """
    Create and show Mrak system tray.
    """
    indicator = AppIndicator.Indicator.new("mrak",
            "weather-overcast-symbolic",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu(app))
    Gtk.main()