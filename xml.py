from dataclasses import dataclass

import xml.etree.cElementTree as ET
from xml.dom import minidom


@dataclass
class Question:
    title: str
    question_text: str
    correct_answer: str
    wrong_answers: list[str]

    def to_xml(self, quiz):
        question = ET.Element("question", type="multichoice")
        ET.SubElement(ET.SubElement(question, "name"), "text").text = self.title
        ET.SubElement(ET.SubElement(question, "questiontext", format="moodle_auto_format"),
                      "text").text = self.question_text
        correct_answer = ET.SubElement(question, "answer", fraction="100", format="html")
        ET.SubElement(correct_answer, "text").text = self.correct_answer
        self.add_feedback(correct_answer)
        for wrong_answer in self.wrong_answers:
            wrong_answer_element = ET.SubElement(question, "answer", fraction="0", format="html")
            ET.SubElement(wrong_answer_element, "text").text = wrong_answer
            self.add_feedback(wrong_answer_element)
        return question

    @staticmethod
    def add_feedback(answer):
        feedback = ET.SubElement(answer, "feedback", format="html")
        ET.SubElement(feedback, "text")

    @staticmethod
    def add_other_elements(question):
        ET.SubElement(ET.SubElement(question, "generalfeedback", format="moodle_auto_format"), "text")
        ET.SubElement(question, "defaultgrade").text = 1.0000000
        ET.SubElement(question, "penalty").text = 0.3333333
        ET.SubElement(question, "hidden").text = 0
        ET.SubElement(question, "single").text = "true"
        ET.SubElement(question, "shuffleanswers").text = "true"
        ET.SubElement(question, "answernumbering").text = "abc"
        ET.SubElement(question, "showstandardinstruction").text = 0
        ET.SubElement(ET.SubElement(question, "correctfeedback", format="html"), "text").text = "Your answer is correct."
        ET.SubElement(question, "partiallycorrectfeedback", format="html")
        ET.SubElement(question, "incorrectfeedback", format="html")
        ET.SubElement(question, "shownumcorrect")


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


if __name__ == '__main__':
    quiz = ET.Element("quiz")
    question = Question("Capital of France", "What is the capital of France?", "Paris", ["Berlin", "London", "Rome"])
    question = question.to_xml(quiz)
    quiz.append(question)
    print(prettify(quiz))
    ET.ElementTree(quiz).write("filename.xml")
