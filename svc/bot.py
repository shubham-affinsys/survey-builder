class SurveyLogic:
    def __init__(self):
        self.slots = {
            "slot_questions": None,  # This should contain the survey data with questions
            "slot_txt": None,
            "slot_options": None,
            "slot_rules": None,
            "slot_user_response": None,
            "slot_survey_completed": "false",
            "q_id": "start",
        }

    def make_question_slots(self):
        """Set up the slots for the current question."""
        if self.slots["slot_questions"] == "null" or not self.slots["slot_questions"]:
            print("No questions available in the survey.")
            self.slots["slot_survey_completed"] = "true"
            return

        if self.slots["q_id"] == "start":
            self.slots["q_id"] = 0

        questions = self.slots["slot_questions"]["questions"]
        q_id = self.slots["q_id"]

        if q_id >= len(questions):
            print("No more questions. Survey completed.")
            self.slots["slot_survey_completed"] = "true"
            return

        # Get the current question
        current_question = questions[q_id]
        self.slots["slot_txt"] = current_question.get("label")
        self.slots["slot_options"] = current_question.get("options", None)
        self.slots["slot_rules"] = current_question.get("rules", None)

        print(f"Question {q_id + 1}: {self.slots['slot_txt']}")
        if self.slots["slot_options"]:
            print(f"Options: {self.slots['slot_options']}")
        else:
            print("No options available for this question.")

    def process_response_and_find_next(self):
        """Process user response using rules to determine the next question."""
        user_response = self.slots.get("slot_user_response")
        if user_response is None:
            print("No user response found.")
            return

        rules = self.slots.get("slot_rules")
        if not rules:
            print("No rules found for the current question. Moving to the next question.")
            self.slots["q_id"] += 1
            return

        # Use jsonLogic to evaluate the rules
        next_questions = get_next_question(rules, {"response": user_response})

        if next_questions:
            # Use the first mapped question as the next question
            next_question_key = next_questions[0]
            questions = self.slots["slot_questions"]["questions"]

            for idx, question in enumerate(questions):
                if question.get("id") == next_question_key:
                    self.slots["q_id"] = idx
                    break
        else:
            print("No valid next question found. Moving to the next sequential question.")
            self.slots["q_id"] += 1

# Import helper functions
from functools import reduce

def jsonLogic(tests, data=None):
    """Evaluate jsonLogic rules."""
    if tests is None or not isinstance(tests, dict):
        return tests

    data = data or {}
    op, values = next(iter(tests.items()))

    operations = {
        "==": lambda a, b: a == b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
        "and": lambda *args: all(args),
        "or": lambda *args: any(args),
        "var": lambda a, not_found=None: reduce(
            lambda d, k: d.get(k, not_found) if isinstance(d, dict) else not_found,
            str(a).split("."),
            data,
        ),
    }

    if op not in operations:
        raise RuntimeError(f"Unrecognized operation '{op}'")

    if not isinstance(values, (list, tuple)):
        values = [values]

    evaluated_values = [jsonLogic(val, data) for val in values]
    return operations[op](*evaluated_values)

def get_next_question(operation, data):
    """Find the next question based on rules."""
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

# Example Flow
if __name__ == "__main__":
    survey_logic = SurveyLogic()

    # Example survey data
    survey_logic.slots["slot_questions"] = {
        "questions": [
            {"id": "q1", "label": "How old are you?", "options": ["<18", "18-24", "25+"], "rules": []},
            {"id": "q2", "label": "What is your gender?", "options": ["Male", "Female"], "rules": []},
            {"id": "q3", "label": "Do you like our service?", "options": ["Yes", "No"], "rules": []},
        ]
    }

    # Start the survey loop
    while survey_logic.slots["slot_survey_completed"] == "false":
        survey_logic.make_question_slots()
        if survey_logic.slots["slot_survey_completed"] == "true":
            break

        # Simulate user response (replace with actual input mechanism)
        survey_logic.slots["slot_user_response"] = input("Your answer: ")

        # Process response and find the next question
        survey_logic.process_response_and_find_next()
