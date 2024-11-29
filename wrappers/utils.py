import requests

def get_ques_ids(questions):
    return [ question.get("id") for question in questions ] 

def map_idx_id(slot_questions):
    return {index: question["id"] for index, question in enumerate(slot_questions.get("questions", []))}


def fetch_questions():
    api_response = requests.get("https://survey-builder-production.up.railway.app/survey_questions/123")
    if api_response.status_code != 200:
        print("Could not fetch questions")
    return api_response.json()



def create_question(q_id,slot_questions):
    if slot_questions == "null":
        print("Question not found")

    else:
        if q_id == "start":
            q_id=0
        
        questions  = slot_questions["questions"]
        current_question = questions[q_id]
        
        slot_txt = current_question.get("label")
        slot_options = current_question.get("options",None)
        slot_rule = current_question.get("rules",None)

        if slot_options is None:
            print("option not found")     
        if slot_rule is None:
            print("Rule not found")

        print("updating utter question and options")
    
    return slot_txt, slot_options, slot_rule