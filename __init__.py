#!/usr/bin/env python
#    This file is part of Acca plugin.

#    Acca plugin is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Acca plugin is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Acca plugin.  If not, see <http://www.gnu.org/licenses/>.

def name():
    return "Acca plugin" 
def description():
    return "Plugin implements ACCA algorithm" 
def qgisMinimumVersion():
    return "1.0" 
def version():
    return "0.1" 
def authorName():
    return "Bastrakov Sergey" 
def classFactory(iface):
    from plugin import Acca_Plugin
    return Acca_Plugin(iface)