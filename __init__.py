def name():
    return "My test plugin"
def description():
    return "NULL"
def qgisMinimumVersion():
    return "1.0"
def version():
    return "Version " + "0.1"
def authorName():
    return "Me"
def classFactory(iface):
    from plugin import TestPlugin
    return TestPlugin(iface)
