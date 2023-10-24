class Quiz:
    def __init__(self,q_list):
        self.question_number = 0
        self.q_list = q_list

    def end_quiz(self):
        return self.question_number < len(self.q_list)

    def next_question(self):
        current_question = self.question_number
        self.question_number +=1
        print(self.question_number,self.q_list[current_question].text, end = " ")
        usr_input = input("True or False ? ").lower()
        return usr_input
    
    def check_answer(self,answer):
        ans = self.q_list[self.question_number-1].answer
        if answer == ans.lower():
            return True
        else:
            return False
