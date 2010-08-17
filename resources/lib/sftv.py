import sys, os, urllib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from resources.lib import media, wall
from resources.lib import plugin


__settings__ = xbmcaddon.Addon(id = 'plugin.video.sf.tv')
getLS = __settings__.getLocalizedString

class Main(object):
    def __init__(self):
        print 'ARGV:', sys.argv
        self.getSettings()
        self.plugin = plugin.PluginFactory.factory()
        mapping = {'wall' : self.wall}
        if self.plugin.pathItems:
            first = self.plugin.pathItems[0]
            if first in mapping:
                mapping[first]()
                return
        self.root()

    def root(self):
        media.Directory().createFolder('News', 'news').createFolder('Wall', 'wall').display()


    def wall(self):
        wall.VideoWall()

    def getSettings(self):
        self.settings = {}
        self.settings['username'] = __settings__.getSetting('username')
        self.settings['password'] = __settings__.getSetting('password')
        self.settings['downloadMode'] = __settings__.getSetting('downloadMode')
        self.settings['downloadPath'] = __settings__.getSetting('downloadPath')
