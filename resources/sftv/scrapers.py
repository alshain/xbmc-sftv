from resources.sftv.server import factory as server_factory
from resources.sftv.media import Directory, VideoFactory
from resources.sftv.util import SfTvClass
from resources.sftv import util
import xbmcgui

class GenericJasonScraper(SfTvClass):
    def __init__(self, function_name):
        super(GenericJasonScraper, self).__init__()
        server = server_factory()
        try:
            json = getattr(server, function_name)()
        except AttributeError:
            self._log('Invalid function name')
            item = xbmcgui.ListItem('No videos.... Try upgrading or come back later')
            Directory().addFile(item, util.currentPath(['..']))
        else:
            self.processJson(json)


    def processJson(self, json):
        dir = Directory()
        for segment in json['segments']:
            id = segment['id']
            info = {}
            info['title'] = segment['title']
            info['thumbnailImage'] = segment['thumb']
            info['date'] = segment['date']
            info['program'] = segment['thumbAlt'][6:].split(' - ')[0]
            video, url = VideoFactory.fromSegmentId(id, info)
            dir.addFile(video, url)

        dir.display()

class ChannelScraper(SfTvClass):
    def __init__(self):
        super(ChannelScraper, self).__init__()
        self.dir = Directory()
        if len(self._plugin.pathItems) >= 2:
            if 'parse' in self._plugin.queryItems:
                self.parseChannel(int(self._plugin.pathItems[1]))
            else:
                self.fastChannel(int(self._plugin.pathItems[1]))
        else:
            self.root()


    def root(self):
        channels = self.getChannels()
        for key, channel in enumerate(channels.findAll('channel')):
            self.dir.createFolder(channel.title.string, str(key))

        self.dir.display()

    def getChannels(self):
        server = server_factory()
        return server.channelsXml()

    def fastChannel(self, channel):
        channel = self.getChannels().findAll('channel')[channel]
        for video in channel.findAll('video'):
            id = video.url.string.split(';id=')[1].split(';')[0]
            info = {}
            info['title'] = video.title.string
            info['program'] = channel.title.string
            info['date'] = video.title.date
            info['thumbnailImage'] = video.image.string.split('?width')[0]
            print id
            video, url = VideoFactory.fromSegmentId(id, info)
            print video
            self.dir.addFile(video, url)

        self.dir.display()

    def parseChannel(self, channel):
        pass

