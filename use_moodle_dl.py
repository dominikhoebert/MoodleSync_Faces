from moodle_dl.moodle.request_helper import RequestHelper
from moodle_dl.moodle.moodle_service import MoodleService
from moodle_dl.moodle.cookie_handler import CookieHandler
from moodle_dl.config import ConfigHelper
from moodle_dl.types import MoodleDlOpts, MoodleURL


def create_request_helper(url: str, username: str, password: str, userid: int):
    moodle_domain, moodle_path = MoodleService.split_moodle_url(url)
    moodle_url = MoodleURL(False, moodle_domain, moodle_path)

    opts = MoodleDlOpts(init=False, config=False, new_token=True, change_notification_mail=False,
                        change_notification_telegram=False, change_notification_xmpp=False, manage_database=False,
                        delete_old_files=False, log_responses=False, add_all_visible_courses=False, sso=False,
                        username=username, password=password, token="", path=".",
                        max_parallel_api_calls=1,
                        max_parallel_yt_dlp=1, max_parallel_downloads=1, max_path_length_workaround=False,
                        download_chunk_size=102400, ignore_ytdl_errors=False, without_downloading_files=False,
                        allow_insecure_ssl=False, skip_cert_verify=False, verbose=True, quiet=False, log_to_file=False,
                        log_file_path=".")
    config = ConfigHelper(opts)

    moodle_token, moodle_private_token = MoodleService(config, opts).obtain_login_token(username=username,
                                                                                        password=password,
                                                                                        moodle_url=moodle_url)
    opts.token = moodle_token
    request_helper = RequestHelper(config=config, opts=opts, moodle_url=moodle_url, token=moodle_token)
    cookie_handler = CookieHandler(request_helper, 2020061500, config, opts)
    cookie_handler.check_and_fetch_cookies(privatetoken=moodle_private_token, userid=str(userid))
    return request_helper
