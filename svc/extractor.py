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

# rule_json = {
#     "and": [
#         {">": [{"var": "input"}, 0]},
#         {"<": [{"var": "input"}, 5]}
#     ]
# }

# user_input = 10
# data = {"input": user_input}

# print(jsonLogic(rule_json, data)) 



# from json_logic import jsonLogic

# Define the operation JSON

true=True
false = False
operation= [
                    {
                        "if": [
                            {
                                "==": [
                                    {
                                        "var": "input"
                                    },
                                    1
                                ]
                            },
                            [
                                {
                                    "update": {
                                        "body": {
                                            "hide": false
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_found"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_improvement"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_often_features"
                                        ]
                                    }
                                }
                            ]
                        ]
                    },
                    {
                        "if": [
                            {
                                "==": [
                                    {
                                        "var": "input"
                                    },
                                    2
                                ]
                            },
                            [
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_found"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": false
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_improvement"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_often_features"
                                        ]
                                    }
                                }
                            ]
                        ]
                    },
                    {
                        "if": [
                            {
                                "==": [
                                    {
                                        "var": "input"
                                    },
                                    3
                                ]
                            },
                            [
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_found"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_improvement"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": false
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_often_features"
                                        ]
                                    }
                                }
                            ]
                        ]
                    }
                ]

# false = False
# true = True
# operation= [
#                     {
#                         "if": [
#                             {
#                                 "and": [
#                                     {
#                                         ">": [
#                                             {
#                                                 "var": "input"
#                                             },
#                                             0
#                                         ]
#                                     },
#                                     {
#                                         "<": [
#                                             {
#                                                 "var": "input"
#                                             },
#                                             5
#                                         ]
#                                     }
#                                 ]
#                             },
#                             [
#                                 {
#                                     "update": {
#                                         "body": {
#                                             "hide": false
#                                         },
#                                         "bodyType": "object",
#                                         "entity": [
#                                             "formsReducer.question_1"
#                                         ]
#                                     }
#                                 },
#                                 {
#                                     "update": {
#                                         "body": {
#                                             "hide": true
#                                         },
#                                         "bodyType": "object",
#                                         "entity": [
#                                             "formsReducer.question3"
#                                         ]
#                                     }
#                                 }
#                             ]
#                         ]
#                     },
#                     {
#                         "if": [
#                             {
#                                 "==": [
#                                     {
#                                         "var": "input"
#                                     },
#                                     9,
#                                     10
#                                 ]
#                             },
#                             [
#                                 {
#                                     "update": {
#                                         "body": {
#                                             "hide": false
#                                         },
#                                         "bodyType": "object",
#                                         "entity": [
#                                             "formsReducer.zysJJRa8kS8gQ5anBcCKQ"
#                                         ]
#                                     }
#                                 },
#                                 {
#                                     "update": {
#                                         "body": {
#                                             "hide": true
#                                         },
#                                         "bodyType": "object",
#                                         "entity": [
#                                             "formsReducer._aiSRKIyr4azr0agHxiWI",
#                                             "formsReducer.D8r_rtGrUG_wROj0PMODt"
#                                         ]
#                                     }
#                                 }
#                             ]
#                         ]
#                     }
#                 ],


def get_next_question(operation, data):
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


# data = {"input": 1}

# next_question = get_next_question(operation, data)
# print(next_question)

def get_all_questions(survey_id):
    from autogen import survey_data

    # survey_data = get_survey_data(survey_id)
    formatted_questions = []

    for question in survey_data:
        f_ques  = {}
        f_ques["id"] = question.get("id")
        f_ques["label"] =  question.get("label")
        f_ques["type"] =  question.get("type")

        if question.get("valuesAllowed",None):
            options  = question.get("valuesAllowed").get("options")
            f_options = []

            for option in options:
                f_option = {}
                f_option["type"] = "payload"
                f_option["title"] = option.get("display_value")
                f_option["payload"] = option.get("api_value")
                f_options.append(f_option)

            f_ques["options"] = f_options

        formatted_questions.append(f_ques)
    return  formatted_questions



if __name__  == "__main__":
    from autogen import survey_data
    all_questions  = get_all_questions("1")

    from pprint import pprint
    pprint(all_questions)
