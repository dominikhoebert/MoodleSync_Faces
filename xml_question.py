from dataclasses import dataclass

from xml.etree import cElementTree as et


@dataclass
class Question:
    title: str
    question_text: str
    correct_answer: str
    wrong_answers: list[str]

    def to_xml(self, quiz):
        question = et.Element("question", type="multichoice")
        et.SubElement(et.SubElement(question, "name"), "text").text = self.title
        et.SubElement(et.SubElement(question, "questiontext", format="markdown"),
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
    def create_category(name: str, info: str = ""):
        category = et.Element("question", type="category")
        et.SubElement(et.SubElement(category, "category"), "text").text = "$course$/top/" + name
        et.SubElement(et.SubElement(category, "info"), "text", format="html").text = info
        et.SubElement(category, "idnumber")
        return category

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
