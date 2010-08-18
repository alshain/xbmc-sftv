import sys
import xbmcplugin
import traceback
from resources.lib import util, config
from resources.lib.server import factory as server_factory
from resources.lib.util import SfTvClass
class VideoWall(SfTvClass):
    '''
    Interface to the videowall.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        server = server_factory()
        xml = server.wall()

        super(SfTvClass, self).__init__()
        sortmethods = (xbmcplugin.SORT_METHOD_LABEL, xbmcplugin.SORT_METHOD_SIZE, xbmcplugin.SORT_METHOD_DATE,
                                 xbmcplugin.SORT_METHOD_VIDEO_RUNTIME, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        for sortmethod in sortmethods:
            print self.plugin.handle, sortmethod
            xbmcplugin.addSortMethod(handle = self.plugin.handle, sortMethod = sortmethod)
        xbmcplugin.setContent(self.plugin.handle, 'movies')
        try:
            for segment in xml.videowall:
                self.parseSegment(segment)
        except Exception, error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print 'ERRORERRORERROR', error, traceback.print_stack(), traceback.print_tb(exc_traceback)
            pass
        xbmcplugin.endOfDirectory(handle = self.plugin.handle, updateListing = True)

    def parseSegment(self, segment):
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
        Video(id, title, id, image, description).add()

    def loadXml(self):
        return util.loadXml(config.wallXml)
