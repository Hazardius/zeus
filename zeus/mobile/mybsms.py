# -*- coding: utf-8 -*-
from __future__ import absolute_import
import uuid
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
import json

from xml.sax.saxutils import escape

escape_dict = {
}


class Client(object):

    apiurl = "https://mybsms.gr/ws/send.json"
    id = "mybsms"
    remote_status = False

    def __init__(self, from_mobile, user, password, dlr_url):
        self.user = user
        self.password = password
        self.from_mobile = from_mobile
        self.delivery_url = dlr_url
        assert self.delivery_url

    def _construct(self, uid, msisdn, message):
        req = {}
        req['username'] = self.user
        req['password'] = self.password
        req['recipients'] = [str(msisdn)]
        message = escape(message, escape_dict)
        req['message'] = message
        if self.delivery_url:
            req['dlr-url'] = self.delivery_url
        req['senderId'] = self.from_mobile
        return req

    def status(self, msgid):
        raise NotImplementedError

    def send(self, mobile, msg, fields={}, uid=None):
        if not uid:
            uid = unicode(uuid.uuid4())

        mobile = mobile.replace("+", "")
        msg = self._construct(uid, mobile, msg)
        data = json.dumps(msg)
        http_response = six.moves.urllib.request.urlopen(self.apiurl, data=data)
        self._last_uid = uid
        try:
            resp = http_response.read()
            response = json.loads(resp)
            status = 'FAIL' if response['error'] else 'OK'

            if status not in ['OK', 'FAIL']:
                return False, "Invalid response status %s" % status
            if status == 'OK':
                return True, response['id']
            else:
                return False, response['error']
        except ValueError:
            return False, "Cannot parse response"
        except KeyError:
            return False, "Cannot read response"
