"""
    SF TV
"""
import sys

#plugin constants
__plugin__ = "SF TV"
__author__ = "alshain"
#__url__ = "http://code.google.com/p/xbmc-addons/"
#__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/TED%20Talks"
__version__ = "0.1"

print "[PLUGIN] '%s: version %s' initialized!" % (__plugin__, __version__)

if __name__ == "__main__":
    import resources.sftv.sftv as sftv
    if not sys.argv[2]:
        sftv.Main()
    elif sys.argv[2].startswith('?addToFavorites'):
        sftv.Main(checkMode = False).addToFavorites(sys.argv[2].split('=')[-1])
    elif sys.argv[2].startswith('?removeFromFavorites'):
        sftv.Main(checkMode = False).removeFromFavorites(sys.argv[2].split('=')[-1])
    elif sys.argv[2].startswith('?downloadVideo'):
        sftv.Main(checkMode = False).downloadVid(sys.argv[2].split('=')[-1])
    else:
        sftv.Main()

sys.modules.clear()
