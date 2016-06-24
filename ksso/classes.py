# -*- coding:utf-8 -*-

import ssl
from django.conf import settings
from .models import *


class PortalController():
    def __init__(self, token):
        self.auth_ctrl = self.AuthController(token)
        self.user_data = self.auth_ctrl.connect()
        self.user_ctrl = self.UserController(self.user_data)
        self.user_data = self.user_ctrl.session()

    def retrieve_user(self):
        return self.user_data

    class UserController():
        class PortalParser():
            def __init__(self, user_data):
                from xml.etree import ElementTree
                self.data = ElementTree.fromstring(user_data).getchildren()[0].getchildren()[0].getchildren()[0]

            # KAIST Portal SSO System 에서 받은 XML 정보를 파싱하여서 리턴합니다.
            def attr(self, item):
                return self.data.find(item).text

        def __init__(self, user_data):
            self.parser = self.PortalParser(user_data)
            self.uid = self.parser.attr('uid')

            # 해당 사용자의 Portal SSO System 정보가 저장되어 있을 경우
            try:
                self.portal_info = PortalInfo.objects.get(uid=self.uid)
                self.update_portal_info()

            # 저장되어 있지 않을 경우
            except PortalInfo.DoesNotExist:
                self.insert_portal_info()
                self.update_portal_info()

        # KAIST Portal SSO System 정보가 저장되어 있지 않을 경우 PortalInfo instance를 생성합니다.
        def insert_portal_info(self):
            from django.contrib.auth.models import User
            user = User.objects.create_user(username=self.uid, password=self.uid)
            user.save()
            self.portal_info = PortalInfo.create(uid=self.uid, user=user)

        # KAIST Portal SSO System 에서 받은 XML 정보를 바탕으로 database를 갱신합니다.
        def update_portal_info(self):
            self.portal_info.uid = self.parser.attr('uid')
            # TODO insert additional data values from portal sso xml
            
            self.portal_info.save()

        def session(self):
            from django.contrib.auth import authenticate
            user = authenticate(username=self.portal_info.user.username, password=self.portal_info.user.username)
            return user

    class AuthController():
        def __init__(self, token):
            from urllib2 import build_opener
            self.token = token
            self.request_string = ''
            self.request_header = []
            self.opener = build_opener()

        # request string 을 만듭니다.
        def build_request_string(self):
            self.request_string = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"'
            self.request_string += ' xmlns:ser="http://server.com">'
            self.request_string += '<soapenv:Header/>'
            self.request_string += '<soapenv:Body>'
            self.request_string += '<ser:verification>'
            self.request_string += '<cookieValue>' + unicode(self.token) + '</cookieValue>'
            self.request_string += '<publicKeyStr>' + unicode(settings.PORTAL_SSO_PUBLIC_KEY) + '</publicKeyStr>'
            self.request_string += '<adminVO>'
            self.request_string += '<adminId>' + unicode(settings.PORTAL_SSO_ADMIN_ID) + '</adminId>'
            self.request_string += '<password>' + unicode(settings.PORTAL_SSO_ADMIN_PW) + '</password>'
            self.request_string += '</adminVO>'
            self.request_string += '</ser:verification>'
            self.request_string += '</soapenv:Body>'
            self.request_string += '</soapenv:Envelope>'

        # request header 를 만듭니다.
        def build_request_header(self):
            self.request_header = [
                ('Content-type', 'text/xml;charset=\"utf-8\"'),
                ('Accept', 'text/xml'),
                ('Cache-Control', 'no-cache'),
                ('Pragma', 'no-cache'),
                ('Content-length', str(len(self.request_string))),
            ]

            self.opener.addheaders = self.request_header

        # urllib2.build_opener를 이용하여 연결합니다.
        def connect(self):
            self.build_request_string()
            self.build_request_header()

            response = self.opener.open(settings.PORTAL_SSO_TARGET_URL, self.request_string).read()
            # 개발을 위해서 Portal SSO System XML 을 직접 보고 싶을 때만 사용하세요.
            # data = PortalData.create(data=response)
            # data.save()

            return response


# combacsa(https://github.com/combacsa)'s Special Hack ends at here


def wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=None,
                ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers=None):

    if ssl_version == None:
        ssl_version = ssl.PROTOCOL_SSLv23

    try:
        return ssl.SSLSocket(sock, keyfile=keyfile, certfile=certfile, server_side=server_side, cert_reqs=cert_reqs,
                 ssl_version=ssl.PROTOCOL_SSLv3, ca_certs=ca_certs, do_handshake_on_connect=do_handshake_on_connect,
                 suppress_ragged_eofs=suppress_ragged_eofs)

    except ssl.SSLError:
        return ssl.SSLSocket(sock, keyfile=keyfile, certfile=certfile, server_side=server_side, cert_reqs=cert_reqs,
                 ssl_version=ssl_version, ca_certs=ca_certs, do_handshake_on_connect=do_handshake_on_connect,
                 suppress_ragged_eofs=suppress_ragged_eofs)


ssl.wrap_socket = wrap_socket

# combacsa(https://github.com/combacsa)'s Special Hack ends at here