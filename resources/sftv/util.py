import urllib2
import cookielib
import os.path
import re
import sys, urllib
from resources.sftv import config, plugin
from BeautifulSoup import BeautifulStoneSoup
from resources.sftv.plugin import PluginFactory
import simplejson
import xbmcplugin

pluginName = sys.modules['__main__'].__plugin__

plugin = PluginFactory.factory()

def loadXml(url):
    """Fetch and parse XML from the given URL"""
    return getXml(loadUrl(url))

def loadUrl(url):
    """Load content from url"""
    request = urllib2.urlopen(url)
    return request.read()

def getJson(json):
    return simplejson.loads(json)

def loadJson(url):
    return getJson(loadUrl(url))

def getXml(xml):
    return BeautifulStoneSoup(xml)

def buildLink(path_items = (), query_items = ()):
    path_items = path_items or list(plugin.pathItems)
    query_items = query_items or {}
    path_items.insert(0, plugin.basePath)
    link = '/'.join(path_items)
    if query_items:
        link += '?' + urllib.urlencode(query_items)
    plugin.log('Building link(%s, %s): %s' % (path_items, query_items, link), 'util')
    return link

def currentPath(subfolders = None, query_items = (), clear_query = False):
    subfolders = listify(subfolders, True)
    step_out = subfolders.count('..')
    log('Pathitems ' + str(plugin.pathItems))
    log('Subfolders ' + str(subfolders))
    if step_out:
        subfolders = plugin.pathItems[:-step_out] + subfolders[step_out:]
    else:
        subfolders = plugin.pathItems + subfolders
    log('Subfolders ' + str(subfolders))
    merged_query = {}
    if not clear_query:
        merged_query = plugin.queryItems.copy()
    merged_query.update(query_items)
    return buildLink(subfolders, merged_query)

def debug():
    #http://wiki.xbmc.org/index.php?title=HOW-TO_debug_Python_Scripts_with_Eclipse
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    print sys.path
    try:
        from pysrc import pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer = True, stderrToServer = True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)

def listify(var, ignore_none = False):
    """Put var in list if it is not a list"""
    log('Listify: %s, %s' % (var, ignore_none))
    if ignore_none and var == None:
        return []
    if not isinstance(var, list):
        var = [var]
    return var

def log(msg):
    plugin.log(msg, 'util')

def filterDictionary(dict, keys):
    filtered = {}
    print dict
    for key, value in dict.iteritems():
        if key in keys:
            filtered[key] = value
    return filtered

def getSetting(key):
    return xbmcplugin.getSetting(PluginFactory.factory().handle, key)

class SfTvClass(object):
    def __init__(self, *args, **kwargs):
        self._plugin = PluginFactory.factory()
        self._log('Constructed')

    def _log(self, msg):
        self._plugin.log(msg, self.__class__.__name__)
