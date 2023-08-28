from moodle_dl.moodle.request_helper import RequestHelper
from moodle_dl.utils import SslHelper
from requests import Session
import urllib
import json

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


def save_auth(auth: dict):
    with open("data/auth.json", "w") as f:
        json.dump(auth, f)


def load_auth():
    with open("data/auth.json", "r") as f:
        return json.load(f)


def get_tokens(username: str, password: str, session: Session):
    data = {'username': username, 'password': password, 'service': 'moodle_mobile_app'}
    response = session.post(f'{url_base}login/token.php', data=urllib.parse.urlencode(data), headers=RQ_HEADER, )
    token = response.json()['token']
    privatetoken = response.json()['privatetoken']
    return token, privatetoken


def get_autologin(token: str, private_token: str, session: Session):
    data = {'moodlewssettingfilter': 'true', 'moodlewssettingfileurl': 'true'}
    data.update({'privatetoken': private_token})
    data.update({'wsfunction': function, 'wstoken': token})
    data = RequestHelper.recursive_urlencode(data)
    url = f'{url_base}webservice/rest/server.php?moodlewsrestformat=json&wsfunction={"tool_mobile_get_autologin_key"}'
    response = session.post(url, data=data, headers=RQ_HEADER)
    print(response.json())
    # TODO catch {'exception': 'moodle_exception', 'errorcode': 'autologinkeygenerationlockout', 'message': 'Das Erzeugen von Auto-Login-Token ist blockiert. Sie müssen {$a} Minuten zwischen den Anforderungen warten.'}
    autologin_key = response.json()['key']
    autologin_url = response.json()['autologinurl']
    return autologin_key, autologin_url


def get_user_id(token: str, session: Session):
    # client.post('core_webservice_get_site_info')
    # _get_POST_DATA request_helper.py 223
    url = f'{url_base}webservice/rest/server.php?moodlewsrestformat=json&wsfunction={"core_webservice_get_site_info"}'
    response = session.post(url, data={'wstoken': token, 'moodlewsrestformat': 'json', 'wsfunction': 'core_webservice_get_site_info'}, headers=RQ_HEADER)
    return response.json()['userid']


def get_cookie(user_id: int, autologin_key: str, autologin_url: str, session: Session):
    data = {'key': autologin_key, 'userid': user_id}
    data_urlencoded = RequestHelper.recursive_urlencode(data)
    response = session.post(autologin_url, data=data_urlencoded, headers=RQ_HEADER)
    return response


def main():
    session = SslHelper.custom_requests_session(False, False)
    # Save Username and Password
    # auth_dict = {"username": username, "password": password}
    # save_auth(auth_dict)

    # Get Tokens
    # auth_dict = load_auth()
    # token, private_token = get_tokens(auth_dict["username"], auth_dict["password"], session)
    # print(f"{token=}, {private_token=}")
    # auth_dict.update({"token": token, "private_token": private_token})
    # save_auth(auth_dict)

    # Get Autologin Key and URL
    # auth_dict = load_auth()
    # print(auth_dict)
    # autologin_key, autologin_url = get_autologin(auth_dict["token"], auth_dict["private_token"], session)
    # print(f"{autologin_key=}, {autologin_url=}")
    # auth_dict.update({"autologin_key": autologin_key, "autologin_url": autologin_url})
    # save_auth(auth_dict)

    # Get User ID
    # auth_dict = load_auth()
    # print(auth_dict)
    # user_id = get_user_id(auth_dict["token"], session)
    # print(user_id)
    # auth_dict.update({"user_id": user_id})
    # save_auth(auth_dict)

    # Get Cookie
    auth_dict = load_auth()
    print(auth_dict)
    response = get_cookie(auth_dict["user_id"], auth_dict["autologin_key"], auth_dict["autologin_url"], session)
    print(response)


if __name__ == '__main__':
    main()
