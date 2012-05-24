"""Python client for Picatcha"""
from urllib2 import urlopen

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
        'customizations': simplejson.dumps(customizations)}

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
    <div id="%(elm_id)s"></div>""" % params


def validate(api_server, params):
    """Validate answers and return response"""
    url = "%s/v" % api_server
    resp_raw = urlopen(url, data=simplejson.dumps(params)).read()
    resp = simplejson.loads(resp_raw)
    return PicatchaResponse(is_valid=(resp.get('s') == True),
        error_code=resp.get('e'))
