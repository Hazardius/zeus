# -*- coding: utf-8 -*-
from __future__ import absolute_import
import uuid
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error

from xml.etree import ElementTree as etree
from xml.sax.saxutils import escape

escape_dict = {
}


def Element(tag, text=None, *args, **kwargs):
    e = etree.Element(tag, *args, **kwargs)
    if text:
        e.text = text
    return e


class Loco(object):

    apiurl = "http://www.locosms.gr/xmlsend.php"
    report_apiurl = "http://www.locosms.gr/input.php"
    remote_status = True
    id = "loco"

    STATUS_MAP = {
        '0': 'Message in queue',
        '1': 'Message Send (delivery status unknown)',
        '2': 'Message Failed',
        '3': 'Message Delivered to Terminal',
        '4': 'Not sent'
    }

    def __init__(self, from_mobile, user, password):
        self.user = user
        self.password = password
        self.from_mobile = from_mobile

    def _cosntruct(self, uid, msisdn, message, fields={}):
        msg = Element("msg")
        msg.append(Element("username", self.user))
        msg.append(Element("password", self.password))
        message = message.decode("utf8")
        message = escape(message, escape_dict)
        msg.append(Element("text", message))
        msg.append(Element("totalfields", str(len(fields.keys()))))

        recipient = Element("recipient")
        recipient.append(Element("uid", uid))
        recipient.append(Element("msisdn", msisdn))
        recipient.append(Element("mobile", self.from_mobile))
        for field, value in fields.iteritems():
            recipient.append(Element(field, value))
        msg.append(recipient)
        return msg

    def status(self, msgid):
        params = {
            'u': self.user,
            'p': self.password,
            'ta': 'ds',
            'slid': msgid,
        }

        post_data = six.moves.urllib.parse.urlencode(params)
        http_response = six.moves.urllib.request.urlopen(self.report_apiurl, data=post_data)
        resp = http_response.read()
        status_code = resp.strip()
        return self.STATUS_MAP.get(status_code)

    def send(self, mobile, msg, fields={}, uid=None):
        if not uid:
            uid = unicode(uuid.uuid4())

        msg = self._cosntruct(uid, mobile, msg, fields)
        _msg = etree.tostring(msg)
        http_response = six.moves.urllib.request.urlopen(self.apiurl, data=_msg)
        self._last_uid = uid
        try:
            resp = http_response.read()
            response = etree.fromstring(resp)
            status = response.find("status").text
            if status not in ['OK', 'FAIL']:
                return False, "Invalid response status %s" % status
            if status == 'OK':
                return True, response.find("smsid").text
            else:
                return False, response.find("reason").text
        except etree.ParseError:
            return False, "Cannot parse response"
