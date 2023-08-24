import shutil

import requests
import re
from moodle_sync_faces import moodle_sync_from_file

login = ""
passwd = ''
# credentials_file = "data/credentials.json"
# url = "https://elearning.tgm.ac.at/pluginfile.php/1548/user/icon/boost_union/f1?rev=76069"
# url = "https://elearning.tgm.ac.at/pluginfile.php/1548/user/icon/lambda/f3"
# filename = "data/faces/test/doppler.jpg"
moodle_index = "https://elearning.tgm.ac.at/login/index.php"
dashboard_url = "https://elearning.tgm.ac.at/my/"
baseurl = "https://elearning.tgm.ac.at"

# ms = moodle_sync_from_file(credentials_file)


# img_data = s.get(url).content
# with open(filename, 'wb') as handler:
#     handler.write(img_data)

client = requests.session()
rememberusername = '1'
data = dict(username=login, password=passwd, rememberusername=rememberusername)
r = client.post(moodle_index, data=data)
if r.status_code is 200:
    res = client.get(baseurl)
    print(res.text)
