import os
import random

from moodle_sync_faces import MoodleSyncFaces
from face import save_faces_json, Face
from xml_question import Question
from xml.etree import cElementTree as et
import cutie

path = "data/"
credentials_file = path + "credentials.json"


def create_questions_from_faces(faces: list[Face]) -> list[Question]:
    questions = []
    for face in faces:
        if not face.ignore_url:
            title = face.group.name + "_" if face.group else ""
            title += str(face.id)
            questions.append(Question(title, f"![{face.fullname}]({face.hd_url})", face.fullname,
                                      get_random_wrong_answers(face, faces, 4)))
    return questions


def get_random_wrong_answers(face: Face, faces: list[Face], n: int) -> list[str]:
    wrong_faces = [f.fullname for f in faces if f != face]
    return random.sample(wrong_faces, n)


def export_questions_to_xml(questions: list[Question], filename: str, category: str = "Faces"):
    quiz = et.Element("quiz")
    quiz.append(Question.create_category(category, "Faces of the course"))
    for question in questions:
        question = question.to_xml(quiz)
        quiz.append(question)
    et.ElementTree(quiz).write(filename)


def main():
    if os.path.isfile(credentials_file):
        ms = MoodleSyncFaces.from_json(credentials_file)
    else:
        print(f"{credentials_file} not found.")
        url = input("Enter Moodle URL: ")
        user = input("Enter username: ")
        password = cutie.secure_input("Enter password: ")
        service = input("Enter service name (ask administrator): ")
        ms = MoodleSyncFaces(url, user, password, service)
    ms.load_courses()
    print("\nSelect course:")
    selected_course = ms.courses[cutie.select([course.fullname for course in ms.courses])]
    course_name = selected_course.fullname.replace(" ", "").replace("/", "")
    ms.get_groups_of_course(selected_course)
    print(selected_course.groups)
    if len(selected_course.groups) > 0:
        print("\nSelect groups: (SPACE to select, ENTER to confirm)")
        selected_groups = cutie.select_multiple([group.name for group in selected_course.groups])
        for group_index in selected_groups:
            group = selected_course.groups[group_index]
            faces = ms.get_faces(selected_course, group)
            filename = path + course_name + "_" + group.name
            export(faces, filename)
    else:
        faces = ms.get_faces(selected_course)
        filename = path + course_name
        export(faces, filename)


def export(faces, filename):
    questions = create_questions_from_faces(faces)
    export_questions_to_xml(questions, filename + ".xml", category="Faces/" + filename)
    print(f"Exported {len(questions)}/{len(faces)} questions to {filename}.xml")
    save_faces_json(faces, filename=filename + ".json")


if __name__ == "__main__":
    main()

# TODOs:
# - [x] read in credentials from file
# - [x] dialog if no credentials file exists
# - [x] simple dialog to select course and group
# - [x] create better file name for faces.json
