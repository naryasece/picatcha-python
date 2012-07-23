"""Python client for Picatcha"""
from urllib2 import urlopen
import random
from datetime import date
import urllib

import simplejson


class PicatchaResponse(object):
    """Response of Picatcha validation request"""
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code


def get_html(api_server, public_key, elm_id='picatcha', customizations=None):
    """Return HTML code for Picatcha widget"""
    if customizations is None:
        customizations = {}
    params = {
        'api_server': api_server,
        'public_key': public_key,
        'elm_id': elm_id,
        'customizations': simplejson.dumps(customizations),
        'session': str((date.today() - date(1970,1,1)).days*86400)+public_key+str(random.randrange(1000000000,9999999999))}
    print params

    return """
    <script type="text/javascript"
        src="%(api_server)s/static/client/picatcha.js"></script>
    <link rel="stylesheet" type="text/css"
        href="%(api_server)s/static/client/picatcha.css" />
    <script>
    Picatcha.API_SERVER = '%(api_server)s';
    Picatcha.PUBLIC_KEY = '%(public_key)s';
    Picatcha.setCustomization(%(customizations)s);
    window.onload = function(){Picatcha.create('%(elm_id)s');}
    </script>
    <div id="%(elm_id)s"></div>
    <noscript>
          <input type="hidden" name="pubkey" value="%(public_key)s" />
          <input type="hidden" name="picatcha_iframe_session" value= "%(session)s" />
          <iframe frameborder="0" width="100%%" height="255px" src="%(api_server)s/nojs?k=%(public_key)s&s=%(session)s">Loading...</iframe>
      </noscript>""" % params
    
    
    

def validate(api_server, params):
    """Validate answers and return response"""
    if 'ses' in params:
        #do no-js validation
        params = urllib.urlencode({'k':params['pk'],'pk':params['k'],'s':params['ses']})
        url = "%s/nojsc" % api_server
        # the k and pk get reversed
        resp_raw = urlopen(url, data=params).read()
        resp = simplejson.loads(resp_raw)
        return PicatchaResponse(is_valid=(resp.get('s') == True), 
            error_code = resp.get('e'))
    
    url = "%s/v" % api_server
    resp_raw = urlopen(url, data=simplejson.dumps(params)).read()
    resp = simplejson.loads(resp_raw)
    return PicatchaResponse(is_valid=(resp.get('s') == True),
        error_code=resp.get('e'))
