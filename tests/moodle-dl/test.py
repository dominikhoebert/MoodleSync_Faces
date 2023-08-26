import urllib

username = ""
password = ''
# url = "https://elearning.tgm.ac.at/pluginfile.php/1548/user/icon/boost_union/f1?rev=76069"
url = "https://elearning.tgm.ac.at/pluginfile.php/1548/user/icon/lambda/f3"
filename = "data/doppler.jpg"
url_base = "https://elearning.tgm.ac.at/"
url_login = "https://elearning.tgm.ac.at/login/index.php"
url_dashboard = "https://elearning.tgm.ac.at/my/"

data = {'username': username, 'password': password, 'service': 'moodle_mobile_app'}
from moodle_dl.utils import SslHelper

session = SslHelper.custom_requests_session(False, False)
RQ_HEADER = {
    'User-Agent': (
            'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPIS26.48-43-2; wv) AppleWebKit/537.36'
            + ' (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 MoodleMobile'
    ),
    'Content-Type': 'application/x-www-form-urlencoded',
}
response = session.post(f'{url_base}login/token.php', data=urllib.parse.urlencode(data), headers=RQ_HEADER,
                        timeout=60)
token = response.json()['token']
privat_token = response.json()['privatetoken']
print(token, privat_token)

from moodle_dl.utils import MoodleDLCookieJar
import os


def get_URL(url: str, cookie_jar_path: str = None):
    """
    Sends a GET request to a specific URL of the Moodle system, including additional cookies
    (cookies are updated after the request)
    @param url: The url to which the request is sent. (the moodle base url is not added to the given URL)
    @param cookie_jar_path: The optional cookies to add to the request
    @return: The resulting Response object.
    """

    session = SslHelper.custom_requests_session(False, False)
    if cookie_jar_path is not None:
        session.cookies = MoodleDLCookieJar(cookie_jar_path)

        if os.path.exists(cookie_jar_path):
            session.cookies.load(ignore_discard=True, ignore_expires=True)
        session.cookies = session.cookies
    try:
        response = session.get(url, headers=RQ_HEADER, timeout=60)
    except Exception as error:
        raise ConnectionError(f"Connection error: {str(error)}") from None

    if cookie_jar_path is not None:
        session.cookies.save(ignore_discard=True, ignore_expires=True)

    return response, session


r, s = get_URL(url, "Cookies.txt")
with open(filename, 'wb') as handler:
    handler.write(r.content)

print(r.text)
