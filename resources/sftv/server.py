import sys
import os
from resources.sftv import util, config
from resources.sftv.plugin import PluginFactory
from BeautifulSoup import BeautifulStoneSoup
import simplejson
from resources.sftv.parser import parse_video_information, parse_wall
class Actual(object):
    """Provide an interface to the world, namely sf.tv"""
    identCache = {}

    def getVideoInfo(self, segment_id):
        url = config.informationBySegment % segment_id
        PluginFactory.factory().log(url, 'server')
        raw = util.loadUrl(url)
        return parse_video_information(raw)

    def getStream(self, fakeUrl):
        #rtmp://cp50792.edgefcs.net/ondemand/mp4:aka/vod/ts20_geb/2010/08/ts20_geb_20100815_192900_web_h264_16zu9_hq1.mp4
        fakeUrl = fakeUrl[7:]
        splitted = fakeUrl.split('/')
        vhost = splitted[0]
        ident_check_url = config.identUrl % vhost
        ident = util.loadXml(ident_check_url)
        server = ident.ip.string
        video = fakeUrl.split('mp4:')[1]
        application = splitted[1]
        params = dict(server = server, app = application, video = video, vhost = vhost)
        print params
        url = config.streamUrl % params
        return url


    def wall(self):
        return util.loadXml(config.wallXml)

class Virtual(object):
    """Emulate Actual's actual responses with predefined content"""
    def __init__(self):
        pass

    def getVideoInfo(self, segment_id):
        f = open(os.path.join(os.getcwd(), "resources", "data", 'video_info.json'))
        return parse_video_information(f.read())

    def getStream(self, fakeUrl):
        identifier = "mp4:aka/vod/ts20/2010/08/ts20_20100815_193000_web_h264_16zu9_mq1.mp4"
        server = "212.243.210.29"
        application = "ondemand"
        auth = "_fcs_vhost=cp50792.edgefcs.net&akmfv=1.7"
        params = dict(server = server, app = application, ident = identifier, auth = auth)
        url = url = "rtmp://%(server)s:1935/%(app)s?%(auth)s playpath=%(ident)s" % params
        url = url + " swfurl=http://www.videoportal.sf.tv/flash/videoplayer.swf swfvfy=1"
        print url
        return url

    def wall(self):
        f = open(os.path.join(os.getcwd(), "resources", "data", 'wall.xml'))
        return parse_wall(f.read())

def factory():
    """Create or return a virtual or actual server"""
    return Actual()
