import os
import json
from requests import post
from face import Face, Group, Course
from use_moodle_dl import create_request_helper


def get_credentials(filename: str):
    with open(filename, "r") as f:
        credentials = json.load(f)
    return credentials["url"], credentials["user"], credentials["password"], credentials["service"]


class MoodleSyncFaces:
    ENDPOINT = "/webservice/rest/server.php"

    def __init__(self, url: str, username: str, password: str, service: str, load_courses: bool = False):
        self.username = username
        self.password = password
        self.url = url
        self.key = self.get_token(username, password, service)
        self.courses = []
        if load_courses:
            self.load_courses()

    @classmethod
    def from_json(cls, filename: str):
        try:
            with open(filename, "r") as f:
                credentials = json.load(f)
        except FileNotFoundError as e:
            print(f"Error: {filename} not found. " + str(e))
            return
        try:
            return MoodleSyncFaces(credentials["url"], credentials["user"], credentials["password"],
                                   credentials["service"])
        except KeyError as e:
            print("Error: Invalid credentials file " + filename, e)

    def get_token(self, username, password, service):
        obj = {"username": username, "password": password, "service": service}
        response = post(self.url + "/login/token.php", data=obj)
        response = response.json()
        return response['token']

    def rest_api_parameters(self, in_args, prefix='', out_dict=None):
        """Transform dictionary/array structure to a flat dictionary, with key names
        defining the structure.

        Example usage:
        rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
        {'courses[0][id]':1,
         'courses[0][name]':'course1'}
        """
        if out_dict is None:
            out_dict = {}
        if not type(in_args) in (list, dict):
            out_dict[prefix] = in_args
            return out_dict
        if prefix == '':
            prefix = prefix + '{0}'
        else:
            prefix = prefix + '[{0}]'
        if type(in_args) == list:
            for idx, item in enumerate(in_args):
                self.rest_api_parameters(item, prefix.format(idx), out_dict)
        elif type(in_args) == dict:
            for key, item in in_args.items():
                self.rest_api_parameters(item, prefix.format(key), out_dict)
        return out_dict

    def call(self, function_name, **kwargs):
        """Calls moodle API function with function name function_name and keyword arguments.

        Example:
        call_mdl_function('core_course_update_courses',
                               courses = [{'id': 1, 'fullname': 'My favorite course'}])
        """
        parameters = self.rest_api_parameters(kwargs)
        parameters.update({"wstoken": self.key, 'moodlewsrestformat': 'json', "wsfunction": function_name})
        response = post(self.url + self.ENDPOINT, parameters)
        response = response.json()
        if type(response) == dict and response.get('exception'):
            raise SystemError("Error calling Moodle API\n", response)
        return response

    def get_faces(self, course: Course, group: Group = None):
        options = [{"name": "groupid", "value": group.id}] if group else None
        response = self.core_enrol_get_enrolled_users(course_id=course.id, options=options)
        faces = [Face.from_dict(f, course, group) for f in response]
        return faces

    def load_courses(self):
        for course in self.core_course_get_recent_courses():
            self.courses.append(Course(course["id"], course["fullname"]))

    def core_course_get_recent_courses(self) -> list[dict]:
        return self.call('core_course_get_recent_courses')

    def core_enrol_get_enrolled_users(self, course_id: int, options=None) -> list[dict]:
        return self.call('core_enrol_get_enrolled_users', courseid=course_id, options=options)

    def core_group_get_course_groups(self, course_id: int):
        return self.call('core_group_get_course_groups', courseid=course_id)

    def get_groups_of_course(self, course: Course):
        response = self.core_group_get_course_groups(course.id)
        course.groups = [Group(group["id"], group["name"]) for group in response]

    def core_webservice_get_site_info(self):
        return self.call("core_webservice_get_site_info")

    def get_user_id(self):
        return self.core_webservice_get_site_info()["userid"]

    def get_request_helper(self):
        # return create_request_helper(self.url, self.username, self.password, self.get_user_id())  # TODO put back in when working
        return create_request_helper(self.url, self.username, self.password, 82)

    def download_faces(self, faces: list, path: str) -> int:
        """Downloads the images of the faces to the given path and returns the number of downloaded images."""
        if not os.path.exists(path):
            os.mkdir(path)

        request_helper = self.get_request_helper()

        counter = 0
        for face in faces:
            if not face.ignore_url:
                counter += 1
                response, _ = request_helper.get_URL(face.hd_url, "Cookies.txt")
                face.filename = str(face.id) + "_" + face.fullname.replace(" ", "_") + "_" + str(face.token) + ".jpg"
                if path:
                    if path[-1] != "/":
                        path += "/"
                face.filename = path + face.filename
                with open(face.filename, 'wb') as handler:
                    handler.write(response.content)
        return counter
