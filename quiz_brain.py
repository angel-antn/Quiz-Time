from data import get_questions


class QuizBrain:

    def __init__(self):

        self.question_bank = get_questions()
        self.question_number = 0
        self.score = 0

    def still_have_questions(self):
        return self.question_number < len(self.question_bank)

    def next_question(self, response):
        self.question_number += 1
        if response == self.question_bank[self.question_number - 1].answer:
            self.score += 1
            return True
        return False

    def get_question(self):
        return self.question_bank[self.question_number].text

    def clean(self):
        self.question_bank = get_questions()
        self.question_number = 0
        self.score = 0
