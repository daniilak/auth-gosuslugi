# -*- coding: utf-8 -*-
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from spv import Auth_SPV
from rosreestr import Auth_LK_Rosreestr

class ApiErr(Exception):
	def __init__(self, exc):
		self.exc = exc

BASE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

class Auth_Gosuslugi:

    def __init__(self, login, password, name_site, user_agent = "") -> None:
        
        self.login          = login
        self.password       = password
        
        self.http           = requests.Session()
        self.cookies = {}
        
        self.base_headers   = {
            "Accept"            : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language"   : "ru-RU,ru;q=0.5",
            "User-Agent"        : user_agent if len(user_agent) != 0 else BASE_USER_AGENT
        }
        self.name_site = name_site

        if self.name_site  == "spv":
            self.site = Auth_SPV(self.base_headers)
        
        if self.name_site  == "rosreestr":
            self.site = Auth_LK_Rosreestr(self.base_headers)
        
        self.auth_url  = self.site.get_url_auth()
        
        

    def auth(self) -> str:
        
        self.__request_get_redirect_url()

        self.__request_auth_url()

        return self.__request_login()

    def __request_get_redirect_url(self):
        """
            Открываем URL авторизации на сайте,
            чтобы получить ссылку на госуслуги с кодом авторизации

            Raises:
                ApiErr: _description_
        """
        try:
            response = self.http.get(
                url             = self.auth_url,
                verify          = False,
                allow_redirects = False,
                headers         = self.base_headers
            )
        except Exception as err:
            raise ApiErr(err)

        if self.name_site == "rosreestr":
            self.site.append_cookies(response.cookies.get_dict())
        self.base_auth_url = response.headers['Location']
    
    def __request_auth_url(self) -> None:
        """
            Открываем базовый auth url в Госуслугах,
            чтобы получить базовые cookies

            Raises:
                ApiErr: _description_
        """
        try:
            response = self.http.get(
                url             = self.base_auth_url,
                verify          = False,
                allow_redirects = False,
                headers         = self.base_headers
            )
        except Exception as err:
            raise ApiErr(err)
        
        self.__set_base_cookies(response.cookies.get_dict())


    def __set_base_cookies(self, cookies : dict) -> None:
        """
            Сохраняем минимальные необходимые для авторизации кукис

            Raises:
                ApiErr: _description_
        """
        try:
            self.cookies = {
                "fhp"               : cookies['fhp'],
                "ESIA_SESSION"      : cookies['ESIA_SESSION'],
                "JSESSIONID"        : cookies['JSESSIONID'],
                "bs"                : cookies['bs'],
                "ctx_id"            : cookies['ctx_id'],
                "sso_segment"       : cookies['sso_segment'],
            }
        except KeyError as err:
            raise ApiErr(err)

    def __request_login(self):
        """
            Делаем основной запрос авторизации в госуслуги
            с передачей логина и пароля

            Raises:
                ApiErr: _description_
        """
        try:
            response = self.http.post(
                url             = "https://esia.gosuslugi.ru/aas/oauth2/api/login",
                cookies         = self.cookies,
                json            = {"login": self.login, "password": self.password},
                verify          = False,
                allow_redirects = False,
                headers         = {
                    "accept": "application/json, text/plain, */*",
                    "accept-language": "ru-RU,ru;q=0.8",
                    "cache-control": "no-cache",
                    "content-type": "application/json",
                    "User-Agent": self.base_headers["User-Agent"]
                }
            )
        except Exception as err:
            raise ApiErr(err)
        
        response = response.json()
        
        if response['action'] != "DONE":
            raise ApiErr("Не удалось авторизоваться...")
        
        return response['redirect_url']

    
    def get_authorized_cookies(self, redirect_url : str):
        """
            Получаем cookies с готовым куки
        """
        return self.site.auth_redirect_url(redirect_url)
