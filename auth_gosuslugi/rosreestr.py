# -*- coding: utf-8 -*-
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from ssl import PROTOCOL_TLS as default_ssl_protocol
except ImportError:
    from ssl import PROTOCOL_SSLv23 as default_ssl_protocol

ssl_context = default_ssl_protocol

class ApiErr(Exception):
	def __init__(self, exc):
		self.exc = exc


class Auth_LK_Rosreestr:

    def __init__(self, base_headers) -> None:
        
        self.base_headers = base_headers
        self.url = "https://lk.rosreestr.ru/"
        
        self.__auth()

    def get_url_auth(self) -> str:
        
        return f"{self.url}account-back/auth/login?homeUrl=https%3A%2F%2Flk.rosreestr.ru%2Flogin"

    def __auth(self):

        try:
            response = requests.get(
                url         = f"{self.url}account-back/profile/roles",
                verify      = False,
                timeout     = 10,
                headers     = {
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": self.base_headers["Accept-Language"],
                    "Pragma": "no-cache",
                    "User-Agent": self.base_headers["User-Agent"],
                }
            )
        except Exception as err:
            raise ApiErr(err)


        cookies = response.cookies.get_dict()
        if f"{self.url}account-back/auth/login?homeUrl=" not in response.text:
            raise ApiErr("Авторизация не нужна")
        
        try:
            self.session_cookies = {
                'session-cookie': cookies['session-cookie'],
                'uid': cookies['uid'],
                'TOMCAT_SESSIONID': cookies['TOMCAT_SESSIONID'],
                'hazelcast.sessionId': cookies['hazelcast.sessionId']
            }
        except KeyError as err:
            raise ApiErr(err)

    def auth_redirect_url(self, redirect_url:str) -> dict:
        try:
            response = requests.get(
                url             = redirect_url,
                cookies         = self.session_cookies,
                verify          = False,
                allow_redirects = False,
                headers         = self.base_headers
            )
        except Exception as err:
            raise ApiErr(err)

        try:
            self.session_cookies["AUTH_TOKEN"] = response.cookies.get_dict()["AUTH_TOKEN"]
        except:
            pass
        
        try:
            self.session_cookies["HOME_URL"] = f"{self.url}login"
        except KeyError as err:
            raise ApiErr(err)
        
        self.session_cookies.pop("STATE")

        self.__check_state()

        return self.session_cookies
    
    def append_cookies(self, cookies):
        try:
            self.session_cookies["STATE"] = cookies["STATE"]
        except KeyError as err:
            raise ApiErr(err)
        
        try:
            self.session_cookies["HOME_URL"] = cookies["HOME_URL"]
        except KeyError as err:
            raise ApiErr(err)

    def __check_state(self):
        try:
            response = requests.get(
                url         = f"{self.url}account-back/config",
                cookies     = self.session_cookies,
                verify      = False,
                headers     = {
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": self.base_headers["Accept-Language"],
                    "Pragma": "no-cache",
                    "User-Agent": self.base_headers["User-Agent"],
                }
            )
        except Exception as err:
            raise ApiErr(err)
        
        try:
            response = requests.get(
                url         = f"{self.url}account-back/profile/roles",
                cookies     = self.session_cookies,
                verify      = False,
                headers     = {
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": self.base_headers["Accept-Language"],
                    "Pragma": "no-cache",
                    "User-Agent": self.base_headers["User-Agent"],
                }
            )
        except Exception as err:
            raise ApiErr(err)

        if int(response.status_code) == 401:
            try:
                response = requests.get(
                    url         = f"{self.url}account-back/config",
                    cookies     = self.session_cookies,
                    verify      = False,
                    headers     = {
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": self.base_headers["Accept-Language"],
                        "Pragma": "no-cache",
                        "User-Agent": self.base_headers["User-Agent"],
                    }
                )
            except Exception as err:
                raise ApiErr(err)
            try:
                self.session_cookies["AUTH_TOKEN"] = response.cookies.get_dict()["AUTH_TOKEN"]
            except:
                pass
            
            try:
                response = requests.get(
                    url         = f"{self.url}account-back/profile/roles",
                    cookies     = self.session_cookies,
                    verify      = False,
                    headers= {
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": self.base_headers["Accept-Language"],
                        "Pragma": "no-cache",
                        "User-Agent": self.base_headers["User-Agent"],
                    }
                )
            except Exception as err:
                raise ApiErr(err)
