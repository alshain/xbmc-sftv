import sys
import xbmcplugin
import traceback
from resources.sftv import util, config
from resources.sftv.server import factory as server_factory
from resources.sftv.util import SfTvClass
from BeautifulSoup import BeautifulStoneSoup
from resources.sftv.media import VideoFactory, Directory
class VideoWall(SfTvClass):
    '''
    Interface to the videowall.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(VideoWall, self).__init__()
        xml = self.getWallXml()
        sortmethods = (xbmcplugin.SORT_METHOD_LABEL, xbmcplugin.SORT_METHOD_SIZE, xbmcplugin.SORT_METHOD_DATE,
                                 xbmcplugin.SORT_METHOD_VIDEO_RUNTIME, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        for sortmethod in sortmethods:
            xbmcplugin.addSortMethod(handle = self._plugin.handle, sortMethod = sortmethod)
        xbmcplugin.setContent(self._plugin.handle, 'movies')
        dir = Directory()
        try:
            for segment in xml.findAll('segment'):
                id, info = self.parseSegment(segment)
                video, url = VideoFactory.fromSegmentId(id, info)
                dir.addFile(video, url)
        except Exception, error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print 'ERRORERRORERROR', error, traceback.print_stack(), traceback.print_tb(exc_traceback)
            pass
        dir.display()
    def getWallXml(self):
        server = server_factory()
        return server.wall()

    def parseSegment(self, segment):
        self._log('Processing segment.')
        id = None
        title = None
        description = None
        image = None
        for element in segment:
            if element.name == 'id':
                id = element.string
            elif element.name == 'description_title':
                description = element.string
            elif element.name == 'sendung':
                title = element.string
            elif element.name == 'image':
                image = element.string
        return (id, {'label' : title, 'title': title, 'thumbnailImage': image, 'label2' : description, 'plot' : description})

    def loadXml(self):
        return util.loadXml(config.wallXml)
