from data import question_data
from question import Question
from quiz_brain import Quiz

question_bank = []
for i in question_data:
    question_bank.append(Question(i["text"],i["answer"]))

abc = Quiz(question_bank)
print(abc.end_quiz())
score = 0
while abc.end_quiz():
    usr_ans = abc.next_question()
    if abc.check_answer(usr_ans):
        score+=1
        print("correct answer",score)
    else:
        print("Incorrect answer",score)