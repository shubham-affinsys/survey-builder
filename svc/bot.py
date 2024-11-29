import json

def nested_to_json(nested_structure):
    """
    Convert a nested list of dictionaries or nested lists into JSON format.

    Args:
        nested_structure (list | dict): A nested list, dict, or combination of both.
    
    Returns:
        dict | list: JSON-compatible nested structure.
    """
    try:
        # Ensure the structure is JSON-serializable
        json_string = json.dumps(nested_structure)
        return json.loads(json_string)
    except TypeError as e:
        raise ValueError(f"Non-serializable data detected: {e}")

# Example usage
nested_data = [
    {"id": 1, "name": "Item 1", "details": {"price": 10.5, "stock": 20}},
    {"id": 2, "name": "Item 2", "details": {"price": 15.0, "stock": 5}},
    [
        {"id": 3, "name": "Item 3"},
        {"id": 4, "name": "Item 4"}
    ]
]

# Get the JSON-compatible structure
json_compatible_data = nested_to_json(nested_data)
print(json.dumps(json_compatible_data))  # Pretty print



# slot_options = [
#         {
#             "title": "Account Services",
#             "type": "payload",
#             "payload": "Account Services"
#         },
#             {
#             "title": "Cheque Services",
#             "type": "payload",
#             "payload": "Cheque Services"
#         },
#             {
#             "title": "Card Services",
#             "type": "payload",
#             "payload": "Card Services"
#         },
#             {
#             "title": "Bot Services",
#             "type": "payload",
#             "payload": "Bot Services"
#         },
#         {
#             "title": "FAQs",
#             "type": "payload",
#             "payload": "faq"
#         }
#     ]

# ques_18625 = {
#   "id":"ques_18625",
#   "project":86,
#   "utter_name":"welcome",
#   "utter_data":{
#     "data":[
#       {
#         "id":"card-0",
#         "list":[
 
#         ],
#         "title":"",
#         "buttons":[
 
#         ],
#         "file_url":"",
#         "subtitle":"How was your expirence with our insurance ploicy?",
#         "frame_url":"",
#         "image_url":"",
#         "list_slot":"",
#         "list_type":"unordered_disc",
#         "video_url":"",
#         "button_slot":"",
#         "post_list_text":""
#       }
#     ],
#     "quick_replies":[

#     ],
#     "template_data":{
#       "template":false,
#       "template_name":"",
#       "template_slots":[
 
#       ],
#       "call_to_action_url":"",
#       "call_to_action_number":""
#     },
#     "quick_replies_slot":"slot_options"
#   },
#   "channel_code":"webchat",
#   "lang":"en",
#   "separate":true,
#   "slots":[
 
#   ],
#   "env":"dev",
#   "category":"flow"
# }

# def make_slot_payload(options):
#     slot_buttons = []
#     btn = {}
#     for option in options:
#         btn = {
#             "title":option.get("value"),
#             "type":"payload",
#             "payload":option.get("sentiment")
#         }
#         slot_buttons.append(btn)
#         btn={}


# slot_survey_data = call_api()

# current_ques_id = None

# if current_ques_id ==  None:
#     current_ques_id == "ques_1"
#     slot_text = slot_survey_data["questions"][current_ques_id]["text"]
#     options = slot_survey_data["questions"][current_ques_id]["options"]

#     slot_buttons = make_slot_payload(options)


# # import uuid

# # def convert_survey_to_cj_json(survey_json):
# #     cj_json = {
# #         "customer_journey_name": survey_json["survey_title"].replace(" ", "_"),
# #         "start_node_id": "",
# #         "nodes": {}
# #     }
    
# #     # Function to generate unique node IDs
# #     def generate_node_id():
# #         return str(uuid.uuid4()).replace("-", "")
    
# #     # Map nodes from survey_json to cj_json
# #     for node_id, node_data in survey_json["nodes"].items():
# #         cj_node = {
# #             "id": generate_node_id(),
# #             "type": node_data["type"],
# #             "metadata": {},
# #             "coordinates": {
# #                 "x": node_data["position"]["x"],
# #                 "y": node_data["position"]["y"]
# #             },
# #             "next": []
# #         }
        
# #         # Set start_node_id if the node is the start node
# #         if node_data["type"] == "start":
# #             cj_json["start_node_id"] = cj_node["id"]

# #         # Handle question nodes
# #         if node_data["type"] == "question":
# #             question_id = node_data["metadata"]["question_id"]
# #             question_data = survey_json["questions"][question_id]

# #             if question_data["type"] == "mcq":
# #                 cj_node["type"] = "utter"
# #                 cj_node["metadata"]["utter_name"] = f"utter_{question_id}"
# #                 cj_node["metadata"]["buttons"] = [
# #                     {"title": option["value"], "payload": option["sentiment"]}
# #                     for option in question_data["data"]["options"]
# #                 ]
# #             elif question_data["type"] == "text_feild":
# #                 cj_node["type"] = "query"
# #                 cj_node["metadata"]["query_text"] = question_data["text"]

# #             # Map next nodes based on sentiment
# #             cj_node["next"] = [
# #                 survey_json["nodes"].get(next_node, {}).get("id", "")
# #                 for sentiment, next_node in question_data["next"].items()
# #                 if next_node
# #             ]
        
# #         # Add node to cj_json
# #         cj_json["nodes"][cj_node["id"]] = cj_node

# #     return cj_json


# # # Example Usage
# # survey_json = {
# #     "survey_title": "Customer Feedback Survey",
# #     "survey_id": "daaa6de1-b965-4f96-b658-e4ed42abc265",
# #     "description": "A survey to collect feedback on customer satisfaction.",
# #     "total_questions": 10,
# #     "nodes": {
# #         "node_111": {
# #             "id": "node_111",
# #             "type": "start",
# #             "name": "start",
# #             "width": 90,
# #             "height": 40,
# #             "position": {
# #                 "x": 12,
# #                 "y": 50
# #             },
# #             "previous": [],
# #             "next": ["node_222"]
# #         },
# #         "node_222": {
# #             "id": "node_222",
# #             "type": "question",
# #             "name": "question_111",
# #             "width": 90,
# #             "height": 40,
# #             "position": {
# #                 "x": 52,
# #                 "y": 100
# #             },
# #             "previous": ["node_111"],
# #             "next": ["node_333", "node_444", "node_555", "node_666"],
# #             "metadata": {
# #                 "question_id": "question_001"
# #             }
# #         }
# #     },
# #     "questions": {
# #         "question_001": {
# #             "type": "mcq",
# #             "text": "How satisfied are you with our service?",
# #             "description": "https://image.url.com/",
# #             "is_required": "true",
# #             "sentiment": "no_sentiment",
# #             "data": {
# #                 "options": [
# #                     {"value": "Very Satisfied", "sentiment": "positive"},
# #                     {"value": "Satisfied", "sentiment": "positive"},
# #                     {"value": "Not Satisfied", "sentiment": "negative"},
# #                     {"value": "Neutral", "sentiment": "neutral"}
# #                 ]
# #             },
# #             "depends_on": [],
# #             "next": {
# #                 "positive": "question_001",
# #                 "negative": "question_002",
# #                 "neutral": "question_003",
# #                 "no_sentiment": "question123"
# #             }
# #         }
# #     }
# # }

# # cj_json = convert_survey_to_cj_json(survey_json)
# # import json
# # print(json.dumps(cj_json, indent=4))
