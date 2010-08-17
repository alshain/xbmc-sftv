import sys
import urllib
import urlparse
path, handle, query = sys.argv
handle = int(handle)

class Plugin(object):
    def __init__(self):
        self.handle = handle
        splitted = path.split('/')
        # ['plugin:', '', 'plugin.video.sf.tv', '']
        self.name = splitted[2]
        self.baseUrl = splitted[0] + '//' + splitted[2] + '/'
        self.pathItems = splitted[3:]
        self.queryItems = {}
        if query:
            self.queryItems = self._parseQuery(query[1:])

    def _parseQuery(self, query):
        self.log('Digesting query string: %s' % query)
        pairs = query.split('&')
        dict = {}
        self.log('pairs ' + str(pairs))
        for pair in pairs:
            name, value = pair.split('=')
            value = urllib.unquote(value)
            dict[name] = value
            self.log(dict)
        return dict

    def log(self, msg, module = 'plugin'):
        msg = unicode(msg).encode('utf-8')
        print '%s:: [%s] %s' % (self.name, module, msg)

class PluginFactory(object):
    plugin = None

    @classmethod
    def factory(cls):
        if not PluginFactory.plugin:
            PluginFactory.plugin = Plugin()
        return PluginFactory.plugin
