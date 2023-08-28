from dataclasses import dataclass

from xml.etree import cElementTree as et
from xml.dom import minidom


@dataclass
class Question:
    title: str
    question_text: str
    correct_answer: str
    wrong_answers: list[str]

    def to_xml(self, quiz):
        question = et.Element("question", type="multichoice")
        et.SubElement(et.SubElement(question, "name"), "text").text = self.title
        et.SubElement(et.SubElement(question, "questiontext", format="moodle_auto_format"),
                      "text").text = self.question_text
        self.add_other_elements(question)
        correct_answer = et.SubElement(question, "answer", fraction="100", format="html")
        et.SubElement(correct_answer, "text").text = self.correct_answer
        self.add_feedback(correct_answer)
        for wrong_answer in self.wrong_answers:
            wrong_answer_element = et.SubElement(question, "answer", fraction="0", format="html")
            et.SubElement(wrong_answer_element, "text").text = wrong_answer
            self.add_feedback(wrong_answer_element)
        return question

    @staticmethod
    def add_feedback(answer):
        feedback = et.SubElement(answer, "feedback", format="html")
        et.SubElement(feedback, "text")

    @staticmethod
    def add_other_elements(question):
        et.SubElement(et.SubElement(question, "generalfeedback", format="moodle_auto_format"), "text")
        et.SubElement(question, "defaultgrade").text = "1.0000000"
        et.SubElement(question, "penalty").text = "0.3333333"
        et.SubElement(question, "hidden").text = 0
        et.SubElement(question, "single").text = "true"
        et.SubElement(question, "shuffleanswers").text = "true"
        et.SubElement(question, "answernumbering").text = "abc"
        et.SubElement(question, "showstandardinstruction").text = 0
        et.SubElement(et.SubElement(question, "correctfeedback", format="html"), "text").text = "Your answer is correct."
        et.SubElement(et.SubElement(question, "partiallycorrectfeedback", format="html"),
                      "text").text = "Your answer is partially correct."
        et.SubElement(et.SubElement(question, "incorrectfeedback", format="html"), "text").text = "Your answer is incorrect."
        et.SubElement(question, "shownumcorrect")


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = et.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


if __name__ == '__main__':
    quiz = et.Element("quiz")
    question = Question("Capital of France", "What is the capital of France?", "Paris", ["Berlin", "London", "Rome"])
    question = question.to_xml(quiz)
    quiz.append(question)
    print(prettify(quiz))
    et.ElementTree(quiz).write("data/filename.xml")
