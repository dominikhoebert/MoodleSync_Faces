import requests
from moodle_sync_faces import moodle_sync_from_file

credentials_file = "../data/credentials_local.json"
ms = moodle_sync_from_file(credentials_file)
response = ms.call("core_webservice_get_site_info")
print(response)

