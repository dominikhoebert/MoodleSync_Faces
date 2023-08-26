from moodle_dl.moodle.request_helper import RequestHelper
from moodle_dl.utils import SslHelper
import urllib

username = ""
password = ''
# url = "https://elearning.tgm.ac.at/pluginfile.php/1548/user/icon/boost_union/f1?rev=76069"
url = "https://elearning.tgm.ac.at/pluginfile.php/1548/user/icon/lambda/f3"
filename = "data/doppler.jpg"
url_base = "https://elearning.tgm.ac.at/"
url_login = "https://elearning.tgm.ac.at/login/index.php"
url_dashboard = "https://elearning.tgm.ac.at/my/"
function = "tool_mobile_get_autologin_key"
RQ_HEADER = {
    'User-Agent': (
            'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPIS26.48-43-2; wv) AppleWebKit/537.36'
            + ' (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 MoodleMobile'
    ),
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {'username': username, 'password': password, 'service': 'moodle_mobile_app'}
session = SslHelper.custom_requests_session(False, False)
response = session.post(f'{url_base}login/token.php', data=urllib.parse.urlencode(data), headers=RQ_HEADER,)
token = response.json()['token']
privatetoken = response.json()['privatetoken']

data = {'moodlewssettingfilter': 'true', 'moodlewssettingfileurl': 'true'}
data.update({'privatetoken': privatetoken})
data.update({'wsfunction': function, 'wstoken': token})
data = RequestHelper.recursive_urlencode(data)
url = f'{url_base}webservice/rest/server.php?moodlewsrestformat=json&wsfunction={function}'
response = session.post(url, data=data, headers=RQ_HEADER)
print(response.json())  # TODO catch {'exception': 'moodle_exception', 'errorcode': 'autologinkeygenerationlockout', 'message': 'Das Erzeugen von Auto-Login-Token ist blockiert. Sie müssen {$a} Minuten zwischen den Anforderungen warten.'}
autologin_key = response.json()['key']
autologin_url = response.json()['autologinurl']

print(autologin_key, autologin_url)



#client.post('core_webservice_get_site_info')
function = 'core_webservice_get_site_info'
data = {'moodlewssettingfilter': 'true', 'moodlewssettingfileurl': 'true'}
data.update({'wsfunction': function, 'wstoken': token})