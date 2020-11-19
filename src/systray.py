'''
A system tray interface for Mrak.
'''

import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Notify, AppIndicator3 as AppIndicator

def menu(mrak):
    '''
    Create the menu for the system tray icon.
    '''

    menu = Gtk.Menu()
    Notify.init("Mrak")

    for remote in mrak.remotes:
        item = Gtk.MenuItem(label=remote.label)
        item.connect("activate", make_display_cmd(remote))
        menu.append(item)

    quitcmd = Gtk.MenuItem(label="Quit Mrak")
    quitcmd.connect("activate", close)
    menu.append(quitcmd)

    menu.show_all()
    return menu

def make_display_cmd(remote):
    def display(_):
            text = f"Remote {remote.name} syncs to {remote.localdir}."
            Notify.Notification.new("Remote", text).show()
    return display

def close(_):
    '''
    Remove Mrak system tray indicator.
    '''
    Gtk.main_quit()

def run(app):
    '''
    Create and show Mrak system tray.
    '''
    indicator = AppIndicator.Indicator.new("mrak",
            "weather-overcast-symbolic",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu(app))
    Gtk.main()