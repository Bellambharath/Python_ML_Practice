class QuizBrain:
    def __init__(self, question_list):
        self.question_number = 0
        self.question_list = question_list
        self.score = 0

    def next_question(self):
        question = self.question_list[self.question_number]
        self.question_number += 1
        user_ans = input(f"Q.{self.question_number} : {question.text} , (True/False) ? ")
        self.check_ans(user_ans, question.answer)

    def still_has_questions(self):

        return len(self.question_list) > self.question_number

    def check_ans(self, user_ans, correct_ans):
        if user_ans.lower() == correct_ans.lower():
            self.score += 1
            print("you got it right")
        else:
            print("you losses it")
        print(f"correct answer is {correct_ans}")
        print(f"your current score is {self.score}/{self.question_number}")
