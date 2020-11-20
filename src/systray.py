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
        item.set_submenu(submenu(remote))
        menu.append(item)

    quitcmd = Gtk.MenuItem(label="Quit Mrak")
    quitcmd.connect("activate", close)
    menu.append(quitcmd)

    menu.show_all()
    return menu

def submenu(remote):
    submenu = Gtk.Menu()

    def show_name(_):
        Notify.Notification.new(remote.label, remote.name).show()
    show_name_item = Gtk.MenuItem(label="Show name")
    show_name_item.connect("activate", show_name)
    submenu.append(show_name_item)

    def show_dir(_):
        Notify.Notification.new(remote.label, remote.localdir).show()
    show_name_item = Gtk.MenuItem(label="Show local sync dir")
    show_name_item.connect("activate", show_dir)
    submenu.append(show_name_item)

    return submenu

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