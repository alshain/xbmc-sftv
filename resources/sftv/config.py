wallXml = "http://www.videoportal.sf.tv/videowallajax"
thumbnailPath = "http://www.sf.tv/piccache/webtool/data/pics/vis/%s/%s/%s/%s_w_h_m.jpg"
informationBySegment = "http://www.videoportal.sf.tv/cvis/segment/%s/filename?nohttperr=1;omit_video_segments_validity=1;omit_related_segments=1;nearline_data=1"
identUrl = "http://%s/fcs/ident"
streamUrl = "rtmp://%(server)s:1935/%(app)s?_fcs_vhost=%(vhost)s&akmfv=1.7 playpath=%(video)s swfurl=http://www.videoportal.sf.tv/flash/videoplayer.swf swfvfy=1"
newestUrl = "http://www.videoportal.sf.tv/pushvideosajax/newest"
bestRatedUrl = "http://www.videoportal.sf.tv/pushvideosajax/bestrated"
mostViewedUrl = "http://www.videoportal.sf.tv/pushvideosajax/mostviews"
dyingUrl = "http://www.videoportal.sf.tv/pushvideosajax/lastchance"
channelsXml = "http://www.videoportal.sf.tv/swf/getchannelteaser"

validInfoKeys = (
    'rating',
    'watched',
    'playcount'
    'overlay',
    'cast',
    'castandrole',
    'director',
    'mpaa',
    'plot',
    'plotoutline',
    'title',
    'duration',
    'studio',
    'tagline',
    'writer',
    'tvshowtitle',
    'premiered',
    'status',
    'code',
    'aired',
    'credits',
    'lastplayed',
    'album',
    'votes',
    'trailer',
)
