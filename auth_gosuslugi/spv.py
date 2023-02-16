# -*- coding: utf-8 -*-
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiErr(Exception):
	def __init__(self, exc):
		self.exc = exc

class Auth_SPV:

    def __init__(self, base_headers) -> None:
        
        self.base_headers = base_headers
        self.url = "https://spv.kadastr.ru/"
        
        self.__auth()

    def get_url_auth(self) -> str:
        
        return f"{self.url}api/v1/login"

    def __auth(self):
        try:
            response = requests.get(
                url         = self.url,
                verify      = False,
                headers     = self.base_headers
            )
        except Exception as err:
            raise ApiErr(err)

        try:
            self.session_cookies = {"session-cookie" : response.cookies.get_dict()['session-cookie']}
        except KeyError as err:
            raise ApiErr(err)

        try:
            response = requests.get(
                url         = f"{self.url}api/v1/user/info/",
                verify      = False,
                cookies     = self.session_cookies,
                headers     = self.base_headers
            )
        except Exception as err:
            raise ApiErr(err)

        try:
            self.session_cookies['XSRF-TOKEN'] = response.cookies.get_dict()['XSRF-TOKEN']
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
            self.session_cookies["JSESSIONID"] = response.cookies.get_dict()["JSESSIONID"]
        except KeyError as err:
            raise ApiErr(err)

        return self.session_cookies
