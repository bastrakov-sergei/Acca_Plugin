#!/usr/bin/env python
def name():
    return "Acca plugin"
def description():
    return "NULL"
def qgisMinimumVersion():
    return "1.0"
def version():
    return "Version " + "0.1"
def authorName():
    return "Bastrakov Sergey"
def classFactory(iface):
    from plugin import Acca_Plugin
    return Acca_Plugin(iface)
