# -*- coding: utf-8 -*-
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from ssl import PROTOCOL_TLS as default_ssl_protocol
except ImportError:
    from ssl import PROTOCOL_SSLv23 as default_ssl_protocol

ssl_context = default_ssl_protocol

BASE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

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
