# -*- coding: utf-8 -*-

from threading import Thread

from gi.repository import Gio, GLib


class Py3status:
    def __init__(self):
        self.urgency = 0
        self.num_notifications = 0

    def post_config_hook(self):
        self._init_dbus()
        self.proxy.call(
            "SignalNotificationCount", None, Gio.DBusCallFlags.NO_AUTO_START, 500, None
        )

    def _init_dbus(self):
        def update(mod, *args):
            n, u = args[-1]
            mod.num_notifications = n
            mod.urgency = u
            mod.py3.update()

        self.bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self.bus.signal_subscribe(
            None,
            "org.freedesktop.Notifications",
            "NotificationsUpdated",
            None,
            None,
            0,
            lambda *args: update(self, *args),
        )
        self.proxy = Gio.DBusProxy.new_sync(
            self.bus,
            Gio.DBusProxyFlags.NONE,
            None,
            "org.freedesktop.Notifications",
            "/org/freedesktop/Notifications",
            "org.freedesktop.Notifications",
            None,
        )

        thread = Thread(target=lambda: GLib.MainLoop().run())
        thread.daemon = True
        thread.start()

    def notifications(self):

        return {
            "cached_until": self.py3.CACHE_FOREVER,
            "full_text": str(self.num_notifications),
            "urgent": self.urgency == 2,
        }

    def on_click(self, event):
        self.proxy.call(
            "ShowNotifications", None, Gio.DBusCallFlags.NO_AUTO_START, 500, None
        )

        return self.notifications()


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    module_test(Py3status)
