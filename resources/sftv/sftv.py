import sys, os, urllib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from resources.sftv import media, wall
from resources.sftv import plugin
from resources.sftv import scrapers


__settings__ = xbmcaddon.Addon(id = 'plugin.video.sf.tv')
getLS = __settings__.getLocalizedString

class Main(object):
    def __init__(self):
        print 'ARGV:', sys.argv
        self.getSettings()
        self.plugin = plugin.PluginFactory.factory()
        mapping = {
            'wall' : (self.wall, [], {}),
            'newest' : (self.genericJson, ['newest'], {}),
            'bestRated' : (self.genericJson, ['bestRated'], {}),
            'mostViewed' : (self.genericJson, ['mostViewed'], {}),
            'dying' : (self.genericJson, ['dying'], {}),
            'channels' : (self.channels, [], {}),
        }
        if self.plugin.pathItems:
            first = self.plugin.pathItems[0]
            if first in mapping:
                func, args, kwargs = mapping[first]
                func(*args, **kwargs)
                return
        self.root()

    def root(self):
        dir = media.Directory().createFolder('Wall', 'wall')
        dir.createFolder('Newest', 'newest')
        dir.createFolder('Best Rated', 'bestRated')
        dir.createFolder('Most Viewed', 'mostViewed')
        dir.createFolder('Dying', 'dying')
        dir.createFolder('Channels', 'channels')
        dir.display()


    def wall(self):
        wall.VideoWall()

    def genericJson(self, function_name):
        scrapers.GenericJasonScraper(function_name)

    def channels(self):
        scrapers.ChannelScraper()




    def getSettings(self):
        self.settings = {}
        self.settings['username'] = __settings__.getSetting('username')
        self.settings['password'] = __settings__.getSetting('password')
        self.settings['downloadMode'] = __settings__.getSetting('downloadMode')
        self.settings['downloadPath'] = __settings__.getSetting('downloadPath')
