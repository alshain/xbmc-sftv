import urllib2
import cookielib
import os.path
import re
import sys, urllib
from resources.lib import config, plugin
from BeautifulSoup import BeautifulStoneSoup
from resources.lib.plugin import PluginFactory

pluginName = sys.modules['__main__'].__plugin__

plugin = PluginFactory.factory()

def loadXml(url):
    """Fetch and parse XML from the given URL"""
    request = urllib2.urlopen(url)
    raw_xml = request.read()
    try:
        return BeautifulStoneSoup(raw_xml)
    except Exception, error:
        print '[%s]' % pluginName, error.args
        raise Exception('Failed to fetch XML')

def buildLink(location = None, parameters = None):
    location = location or plugin.location
    parameters = parameters or {}
    link = plugin.baseUrl + location
    if parameters:
        link += '?' + urllib.urlencode(parameters)
    plugin.log('Building link(%s, %s): %s' % (location, parameters, link), 'util')
    return link

class SfTvClass(object):
    def __init__(self, *args, **kwargs):
        self._plugin = PluginFactory.factory()
        self._log('Constructed')

    def _log(self, msg):
        self._plugin.log(msg, self.__class__.__name__)
