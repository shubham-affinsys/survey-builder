from utils import *


# fetch questions
slot_questions = fetch_questions()
print(slot_questions)
# initialize slots
q_id="start"



# map index to question id
mapper = map_idx_id(slot_questions.get("questions"))


user_response = "start"


not_answered = get_ques_ids(slot_questions)

print(not_answered)
answered = []

# fill slots 

# while( rem_ques!=0 and user_response!="cancel" ):
