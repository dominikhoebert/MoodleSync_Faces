from moodle_dl.moodle.request_helper import RequestHelper
from moodle_dl.utils import SslHelper

key_data = {'key': '',
            'autologinurl': 'https://elearning.tgm.ac.at/admin/tool/mobile/autologin.php', 'warnings': []}
autologin_key = key_data['key']
autologin_url = key_data['autologinurl']
cookie_jar_path = "Cookies_test.txt"
userid = 82

print(autologin_key, autologin_url)
RQ_HEADER = {
    'User-Agent': (
            'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPIS26.48-43-2; wv) AppleWebKit/537.36'
            + ' (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 MoodleMobile'
    ),
    'Content-Type': 'application/x-www-form-urlencoded',
}


# cookie_handler.py 80
data = {'key': autologin_key, 'userid': userid}
url = autologin_url

data_urlencoded = RequestHelper.recursive_urlencode(data)
session = SslHelper.custom_requests_session(False, False)
response = session.post(url, data=data_urlencoded, headers=RQ_HEADER)

# if cookie_jar_path is not None:
#     for cookie in session.cookies:
#         cookie.expires = 2147483647
#
#     session.cookies.save(ignore_discard=True, ignore_expires=True)

print(response.url)


