from resources.sftv.util import getJson, getXml
def parse_video_information(raw):
    raw = raw.splitlines()[1]
    return getJson(raw)

def parse_wall(raw):
    return getXml(raw)

