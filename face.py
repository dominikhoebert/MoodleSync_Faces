import os
import random
import json
from requests import get
from dataclasses import dataclass


def generate_token():
    return random.randint(10000, 99999)


def face_from_dict(face_dict: dict, course=None, group=None):
    try:
        face = Face(face_dict["id"], face_dict["firstname"], face_dict["lastname"],
                    face_dict["fullname"], face_dict["email"], face_dict["profileimageurl"])
    except KeyError as e:
        raise KeyError("Face dict must contain keys 'id', 'fullname', 'profile_url' and 'image_url' " + str(e))
    if course:
        face.course = course
    if group:
        face.group = group
    return face


def download_faces(faces: list, path: str = None):
    if not os.path.exists(path):
        os.mkdir(path)
    for face in faces:
        img_data = get(face.image_url).content
        face.filename = str(face.id) + "_" + face.fullname.replace(" ", "_") + "_" + str(face.token) + ".jpg"
        if path:
            if path[-1] != "/":
                path += "/"
            face.filename = path + face.filename
        with open(face.filename, 'wb') as handler:
            handler.write(img_data)


def save_faces_json(faces: list, filename: str = None):
    faces_dict = {"faces": [face.__dict__() for face in faces]}
    if filename:
        with open(filename, "w") as f:
            json.dump(faces_dict, f)
    return faces_dict


class Face:
    def __init__(self, id: int,firstname: str, lastname: str, fullname: str, email: str,
                 image_url: str):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = fullname
        self.email = email
        self.profile_url = None
        self.image_url = image_url
        self.token = generate_token()
        self.filename = None
        self.tags = []
        self.course = None
        self.group = None

    def __repr__(self):
        return (f"Face(id: {self.id}, fullname: {self.fullname}, email: {self.email}, image_url: {self.image_url}, "
                f"filename: {self.filename}, {self.tags}, {self.course.fullname if self.course else None}, "
                f"{self.group.name if self.group else None})")

    def __dict__(self):
        return {"id": self.id, "firstname": self.firstname, "lastname": self.lastname,
                "fullname": self.fullname, "email": self.email, "profile_url": self.profile_url,
                "image_url": self.image_url, "token": self.token, "filename": self.filename, "tags": self.tags,
                "course_id": self.course.id if self.course else None,
                "course_name": self.course.fullname if self.course else None,
                "group_id": self.group.id if self.group else None,
                "group_name": self.group.name if self.group else None}


@dataclass
class Group:
    id: int
    name: str


@dataclass
class Course:
    id: int
    fullname: str
    groups: list[Group] = None
