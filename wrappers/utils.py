import requests

def get_all_qid(slot_questions):
    return [id for id in slot_questions]


def fetch_questions():
    # api_response = requests.get("https://survey-builder-production.up.railway.app/survey_questions/123")
    api_response = requests.get("http://127.0.0.1:8080/survey_questions/123")
    if api_response.status_code != 200:
        print("Could not fetch questions")
    return api_response.json()



def create_question(q_id,slot_questions):
    current_question = slot_questions.get(q_id)
        
    slot_txt = current_question.get("label")
    slot_options = current_question.get("options",None)
    slot_rule = current_question.get("rules",None)

    # if slot_options is None:
        # print("option not found")     
    # if slot_rule is None:
        # print("Rule not found")

    # print("updating utter question and options")
    
    return slot_txt, slot_options, slot_rule



import sys
from functools import reduce

def jsonLogic(tests, data=None):
    # Base case: return primitive values as-is
    if tests is None or not isinstance(tests, dict):
        return tests

    data = data or {}

    # Extract the operation and its arguments
    op, values = next(iter(tests.items()))

    # Supported operations
    operations = {
        "==": lambda a, b: a == b,
        "===": lambda a, b: a is b,
        "!=": lambda a, b: a != b,
        "!==": lambda a, b: a is not b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "<": lambda a, b, c=None: a < b if c is None else a < b < c,
        "<=": lambda a, b, c=None: a <= b if c is None else a <= b <= c,
        "!": lambda a: not a,
        "and": lambda *args: all(args),
        "or": lambda *args: any(args),
        "?": lambda a, b, c: b if a else c,
        "var": lambda a, not_found=None: reduce(
            lambda d, k: d.get(k, not_found) if isinstance(d, dict) else not_found,
            str(a).split("."),
            data,
        ),
    }

    if op not in operations:
        raise RuntimeError(f"Unrecognized operation '{op}'")

    # Ensure values are a list for unary operators or single arguments
    if not isinstance(values, (list, tuple)):
        values = [values]

    # Recursively evaluate arguments
    evaluated_values = [jsonLogic(val, data) for val in values]

    # Apply the operation with evaluated arguments
    return operations[op](*evaluated_values)



def get_next_question(operation, data):
    try:
        next_question = []
        for op in operation:
            if "if" in op:
                condition, actions = op["if"]
                if jsonLogic(condition, data):
                    for action in actions:
                        if "update" in action and not action["update"]["body"]["hide"]:
                            entity = action["update"]["entity"][0]
                            next_question.append(entity.split(".")[-1])  
                    break
        return next_question
    except Exception as e:
        print(f"error while getiing next  question {e}")
        return []

def get_hidden_question_ids(rules):
    hidden_ids = []
    for rule in rules:
        if "if" in rule:
            _, actions = rule["if"]  # Extract the actions part of the rule
            for action in actions:
                if "update" in action:
                    update = action["update"]
                    body = update.get("body", {})
                    
                    # Check if 'hide' is true
                    if body.get("hide") == True:
                        # Extract entity IDs
                        for entity in update.get("entity", []):
                            # Remove 'formsReducer.' prefix if present
                            hidden_ids.append(entity.replace("formsReducer.", ""))
    
    return hidden_ids

# def get_hidden_question_ids(rules):
#     hidden_ids = []

#     # Iterate through each rule
#     for rule in rules:
#         for condition in rule.get('if', []):
#             # Check if the condition is an equality check on 'input'
#             if isinstance(condition, dict) and '==' in condition:
#                 equality_condition = condition['==']
#                 if isinstance(equality_condition, list) and len(equality_condition) == 2:
#                     actions = equality_condition[1]  # Actions are after the condition
                
#                     # If actions exist, iterate through them
#                     if isinstance(actions, list):
#                         for action in actions:
#                             update = action.get('update', {})
#                             body = update.get('body', {})
                            
#                             # Check if 'hide' is true
#                             if body.get('hide') == True:
#                                 # Look for 'entity' in body, which represents the question IDs
#                                 for entity in body.get('entity', []):
#                                     # Remove 'formsReducer.' prefix, if present
#                                     hidden_ids.append(entity.replace('formsReducer.', ''))
    
#     return hidden_ids