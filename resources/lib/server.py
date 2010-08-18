import sys
import os
class Actual(object):
    """Provide an interface to the world, namely sf.tv"""

    def getVideoInfo(self, segment_id):
        pass
    
    def wall(self):
        pass
    
class Virtual(object):
    """Emulate Actual's actual responses with predefined content"""
    def __init__(self):
        pass
    
    def getVideoInfo(self, segment_id):
        f = open(os.path.join(os.getcwd(), "resources", "data", 'video_info.json'))
        return f.read()
    
    def wall(self):
        f = open(os.path.join(os.getcwd(), "resources", "data", 'wall.xml'))
        return f.read()
    
def factory():
    """Create or return a virtual or actual server"""
    return Virtual()
        