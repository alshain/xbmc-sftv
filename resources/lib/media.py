import xbmcplugin, xbmcgui
from resources.lib import plugin, util, config
from resources.lib.server import factory as server_factory
import urllib
from resources.lib.util import SfTvClass
import re

class VideoFactory(SfTvClass):
    @classmethod
    def fromSegmentId(cls, segment_id, info):
        plugin.PluginFactory.factory().log('Loading from segmentid', 'media')
        server = server_factory()
        json = server.getVideoInfo(segment_id)
        return VideoFactory.fromVideoInfo(json, info)

    @classmethod
    def fromVideoInfo(cls, json, info = None):
        """Return tuple(video item, url)"""
        server = server_factory()
        if not info:
            info = {'label' : json['description_title'], 'title' : json['description_title']}
        date = ('1', '1', '1970')
        if 'time_published' in json:
            time_published = json['time_published']
            date = VideoFactory.convertDate(time_published)
        info['date'] = "%s.%s.%s" % date
        info['year'] = date[2]

        bitrate = 0
        selected_stream = 0
        for key, stream in enumerate(json['streaming_urls']):
            if stream['bitrate'] > bitrate:
                selected_stream = key
        stream = json['streaming_urls'][selected_stream]
        url = server.getStream(stream['url'])
        return (Factory.video(info), url)

    @classmethod
    def convertDate(cls, date):
        """Return (d, m, Y)"""
        #%d.%m.%Y / 01.01.2009
        #2010-08-15 19:29:00
        m = re.match(r"([\d]{4})-(\d\d)-(\d\d)", date)
        return (m.group(2), m.group(1), m.group(0))



class Factory(object):
    @classmethod
    def video(cls, info = None):
        return Factory.item(kwargs = info, info = info, type = 'video')

    @classmethod
    def folder(cls, info = None):
        return Factory.item(kwargs = info, info = info)

    @classmethod
    def item(cls, kwargs = None, info = None, properties = None, type = 'video'):
        kwargs = kwargs or {'label' : '_undefined'}
        item = xbmcgui.ListItem(**Factory._filterItemKwargs(kwargs))
        print 'Label', item.getProperty('label')
        if info:
            item.setInfo(type, info)
        if properties:
            for key, value in properties.iteritems():
                item.setProperty(key, value)
        return item

    @classmethod
    def _filterItemKwargs(cls, kwargs):
        allowed = ('label', 'label2', 'thumbnailImage', 'iconImage', 'path')
        filtered = {}
        for key in allowed:
            if key in kwargs:
                filtered[key] = kwargs[key]
        return filtered

class Directory(SfTvClass):
    def __init__(self):
        super(Directory, self).__init__()
        self._dir = []

    def addFile(self, item, path):
        self.addItem(item, path, False)
        return self

    def addFolder(self, item, path):
        self.addItem(item, path, True)
        return self

    def createVideo(self, info):
        self.addFile(Factory.video(info), info['path'])
        return self

    def createFolder(self, name, path, info = None, is_plugin_subfolder = True):
        """Create new folder in directory list
        
        Create and add a folder to the current directory and assume that it is 
        a plugin of the current folder
        
        """
        if is_plugin_subfolder:
            path = util.currentPath(path)
        info = info or {}
        info.update({'label' : name})
        self.addFolder(Factory.folder(info), path)
        return self

    def addItem(self, item, path, is_folder = False):
        """Add an item to the current directory"""
        self._dir.append((item, path, is_folder))
        return self

    def display(self):
        """Send all items to XBMC and display it"""
        for args in self._dir:
            self._displayItem(*args)
        xbmcplugin.endOfDirectory(self._plugin.handle, cacheToDisc = False)
        return self

    def _displayItem(self, item, path, is_folder):
        """Register a single item with XBMC"""
        if not item.getProperty('url'):
            self._log('No url set')
        else:
            self._log('Displaying item %s' % path)
        print item
        xbmcplugin.addDirectoryItem(self._plugin.handle, path, item, isFolder = is_folder)
