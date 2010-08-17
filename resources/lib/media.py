import xbmcplugin, xbmcgui
from resources.lib import plugin, util, config
import urllib
from resources.lib.util import SfTvClass

class VideoFactory(SfTvClass):
    def __init__(self):
        super(VideoFactory, self).__init__()

    @classmethod
    def bySegment(self, segment_id):
        xml = util.loadXml(config.informationBySegment % segment_id)

class Folder(SfTvClass):
    def __init__(self, name, path):
        super(Folder, self).__init__()
        self.item.path = util.buildLink(path, {'url' : path})

class Factory(object):
    @classmethod
    def video(cls, info = None):
        return Factory.item(info, 'video')

    @classmethod
    def folder(cls, info = None):
        return Factory.item(info)

    @classmethod
    def item(cls, kwargs = None, info = None, properties = None, type = 'video'):
        kwargs = kwargs or {'label' : '_undefined'}
        item = xbmcgui.ListItem(**Factory._filterItemKwargs(kwargs))
        if info:
            item.setInfo(type, info)
        if properties:
            for key, value in info.iteritems():
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

    def addFile(self, item, url):
        self.addItem(item, url, False)
        return self

    def addFolder(self, item, url):
        self.addItem(item, url, True)
        return self

    def createVideo(self, info):
        self.addFile(Factory.video(info), info['url'])
        return self

    def createFolder(self, name, url, info = None):
        info = info or {}
        info.update({'label' : name, 'url' : url})
        self.addFolder(Factory.folder(info), info['url'])
        return self

    def addItem(self, item, url, is_folder = False):
        self._dir.append((item, url, is_folder))
        return self

    def display(self):
        for item, url, is_folder in self._dir:
            self._displayItem(item, url, is_folder)
        xbmcplugin.endOfDirectory(self._plugin.handle, cacheToDisc = False)
        return self

    def _displayItem(self, item, url, is_folder):
        self._log('Displaying item %s' % url)
        print item
        xbmcplugin.addDirectoryItem(handle = self._plugin.handle, url = url, listitem = item, isFolder = is_folder)
