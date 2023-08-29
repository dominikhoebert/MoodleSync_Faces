import random

from moodle_sync_faces import MoodleSyncFaces
from face import save_faces_json, Face
from xml_question import Question
from xml.etree import cElementTree as et

# credentials_file = "data/credentials_local.json"
credentials_file = "data/credentials.json"
faces_json = "data/faces.json"
xml_path = "data/"


def create_questions_from_faces(faces: list[Face]) -> list[Question]:
    questions = []
    for face in faces:
        title = face.group.name + "_" if face.group else ""
        title += face.id
        questions.append(Question(title, f"![{face.fullname}]({face.hd_url})", face.fullname, []))
    return questions


def get_random_wrong_answers(face: Face, faces: list[Face], n: int) -> list[Face]:
    wrong_faces = [f for f in faces if f != face]
    return random.sample(wrong_faces, n)


def export_questions_to_xml(questions: list[Question], filename: str):
    quiz = et.Element("quiz")
    for question in questions:
        question = question.to_xml(quiz)
        quiz.append(question)
    et.ElementTree(quiz).write(filename)


def main():
    ms = MoodleSyncFaces.from_json(credentials_file)
    ms.load_courses()
    print(ms.courses)
    ms.get_groups_of_course(ms.courses[0])
    print(ms.courses[0].groups)
    faces = ms.get_faces(ms.courses[0], ms.courses[0].groups[0])
    filename = xml_path + ms.courses[0].fullname + "_" + ms.courses[0].groups[0].name + ".xml"
    questions = create_questions_from_faces(faces)
    export_questions_to_xml(questions, filename)
    # successful_downloads = ms.download_faces(faces, path=faces_path)
    # print(f"{successful_downloads}/{len(faces)} faces downloaded successfully.")
    save_faces_json(faces, filename=faces_json)
    # print(ms.upload_files(faces_json, file_path='/', file_area='draft', item_id=0))


if __name__ == "__main__":
    main()
