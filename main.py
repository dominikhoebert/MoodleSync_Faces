import random

from moodle_sync_faces import MoodleSyncFaces
from face import save_faces_json, Face
from xml_question import Question
from xml.etree import cElementTree as et

credentials_file = "credentials.json"


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
    ms = MoodleSyncFaces.from_json(credentials_file)
    ms.load_courses()
    print(ms.courses)
    ms.get_groups_of_course(ms.courses[0])
    print(ms.courses[0].groups)
    faces = ms.get_faces(ms.courses[0], ms.courses[0].groups[0])
    filename = (ms.courses[0].fullname.replace(" ", "").replace("/", "") + "_" +
                ms.courses[0].groups[0].name + ".xml")
    questions = create_questions_from_faces(faces)
    print(f"Exported {len(questions)}/{len(faces)} questions to {filename}")
    export_questions_to_xml(questions, filename, category="Faces_" + ms.courses[0].fullname)
    save_faces_json(faces, filename="faces.json")  # TODO create better file name


if __name__ == "__main__":
    main()

# TODOs:
# - [ ] read in credentials from file
# - [ ] dialog if no credentials file exists
# - [ ] simple dialog to select course and group
# - [ ] create better file name for faces.json
