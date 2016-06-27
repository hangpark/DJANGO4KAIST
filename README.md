# ksso
KAIST Single Auth Service 3.0 with Django
======
This branch is for **Python 3.5**. Other versions of python 3 were not tested yet.

Check [KAIST Single Auth Service v3.0](http://ctreq.kaist.ac.kr/static/docs/guide.pdf) official document.

**Tested with** Python 3.5.1, Django 1.9.7, requests 2.10.0 on Ubuntu 16.0.4.

## Install
It is recommended to use `virtualenv` to make your python project would be independent to others.
```sh
$ cd {BASE_DIR of your django project}
$ git clone -b support/python-3.5 https://github.com/HangPark/DJANGO4KAIST
$ mv DJANGO4KAIST/ksso .
$ pip install DJANGO4KAIST/requirements.txt
$ rm -rf DJANGO4KAIST
```

## Settings
- Add this app into your django project by editting `settings.py` of it.
- Configure `ksso/settings.py` variables:
    
    - `PORTAL_ADMIN_ID` - Portal ID of a person can access the system. (usually the manager of your site)
    - `PORTAL_ADMIN_PW` - Portal password of a person can access the system.
    - `PORTAL_PUBLIC_KEY` - Public key of your site issued by KAIST
    - `PORTAL_LOGIN_URL` - Login page of KAIST single auth system.
    - `PORTAL_TARGET_URL` - Targeting page for SOAP request to get user infos.
    - `AUTH_REDIRECT_URL` - Default url after authorization if redirection url was not given.

- Implement `TODO` in `ksso/models.py` and `ksso/classes.py` for additional SOAP fields.
- `python makemigrations ksso`
- `python migrate ksso`
- Attach `ksso.views.LoginView` and `ksso.views.LogoutView` to your login & out url, respectively by using `as_view()` in `urls.py` of your project like below:
```python
...
from ksso.views import LoginView, LogoutView
...
urlpatterns = [
    ...
    url(r'^user/login/$', LoginView.as_view()),
    url(r'^user/logout/$', LogoutView.as_view()),
    ...
]
```

## Improved Features
In comparison to the previous version, `requests` module is used instead of `urllib` or `urllib2`. Moreover, it became possible to specify a redirection url after authrization.

### Redirection URL
To specify redirection url after authrization, you can add it to the GET parameter `next`. For example, if the login url is `/user/login` and user should move to `/article/123` after login successful, you can use `/user/login?next=/article/123` for login url.

This feature is implemented by using cookie named `REDIRECT_URL_TOKEN` because the KAIST single auth service can not pass the custom redirect url.