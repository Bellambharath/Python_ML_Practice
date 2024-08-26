from data import question_data
from question_model import Question
from quiz_brain import QuizBrain

print(len(question_data))

question_bank = []

for key in question_data:
    question = Question(key['text'], key['answer'])
    question_bank.append(question)

quiz_brain = QuizBrain(question_bank)
while quiz_brain.still_has_questions():
    quiz_brain.next_question()




