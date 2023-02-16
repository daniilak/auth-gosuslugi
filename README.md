# Authorization on sites through gosuslugi using requests

## What does it do?
Saves the necessary cookies to work with sites where there is authorization through gosuslugi.ru

## List of sites where it works

- spv.kadastr.ru
- rosreestr.ru
- lk.rosreestr.ru

## Installation
```bash
pip install auth_gosuslugi
```

## Usage

If the authorization to the site spv.kadastr.ru
```python
from auth_gosuslugi.auth import Auth_Gosuslugi
ga = Auth_Gosuslugi("+7 (910) 123-456-78", "password_here", "spv", user_agent="")
redirect_url = ga.auth()
cookies = ga.get_authorized_cookies(redirect_url)
print(cookies)
```
If the authorization to the site rosreestr.ru
```python
from auth_gosuslugi.auth import Auth_Gosuslugi
ga = Auth_Gosuslugi("+7 (910) 123-456-78", "password_here", "rosreestr", user_agent="")
redirect_url = ga.auth()
cookies = ga.get_authorized_cookies(redirect_url)
print(cookies)
```

```
Default user agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
```
You can replace with any other user agent
