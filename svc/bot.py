import uuid

def convert_survey_to_cj_json(survey_json):
    cj_json = {
        "customer_journey_name": survey_json["survey_title"].replace(" ", "_"),
        "start_node_id": "",
        "nodes": {}
    }
    
    # Function to generate unique node IDs
    def generate_node_id():
        return str(uuid.uuid4()).replace("-", "")
    
    # Map nodes from survey_json to cj_json
    for node_id, node_data in survey_json["nodes"].items():
        cj_node = {
            "id": generate_node_id(),
            "type": node_data["type"],
            "metadata": {},
            "coordinates": {
                "x": node_data["position"]["x"],
                "y": node_data["position"]["y"]
            },
            "next": []
        }
        
        # Set start_node_id if the node is the start node
        if node_data["type"] == "start":
            cj_json["start_node_id"] = cj_node["id"]

        # Handle question nodes
        if node_data["type"] == "question":
            question_id = node_data["metadata"]["question_id"]
            question_data = survey_json["questions"][question_id]

            if question_data["type"] == "mcq":
                cj_node["type"] = "utter"
                cj_node["metadata"]["utter_name"] = f"utter_{question_id}"
                cj_node["metadata"]["buttons"] = [
                    {"title": option["value"], "payload": option["sentiment"]}
                    for option in question_data["data"]["options"]
                ]
            elif question_data["type"] == "text_feild":
                cj_node["type"] = "query"
                cj_node["metadata"]["query_text"] = question_data["text"]

            # Map next nodes based on sentiment
            cj_node["next"] = [
                survey_json["nodes"].get(next_node, {}).get("id", "")
                for sentiment, next_node in question_data["next"].items()
                if next_node
            ]
        
        # Add node to cj_json
        cj_json["nodes"][cj_node["id"]] = cj_node

    return cj_json


# Example Usage
survey_json = {
    "survey_title": "Customer Feedback Survey",
    "survey_id": "daaa6de1-b965-4f96-b658-e4ed42abc265",
    "description": "A survey to collect feedback on customer satisfaction.",
    "total_questions": 10,
    "nodes": {
        "node_111": {
            "id": "node_111",
            "type": "start",
            "name": "start",
            "width": 90,
            "height": 40,
            "position": {
                "x": 12,
                "y": 50
            },
            "previous": [],
            "next": ["node_222"]
        },
        "node_222": {
            "id": "node_222",
            "type": "question",
            "name": "question_111",
            "width": 90,
            "height": 40,
            "position": {
                "x": 52,
                "y": 100
            },
            "previous": ["node_111"],
            "next": ["node_333", "node_444", "node_555", "node_666"],
            "metadata": {
                "question_id": "question_001"
            }
        }
    },
    "questions": {
        "question_001": {
            "type": "mcq",
            "text": "How satisfied are you with our service?",
            "description": "https://image.url.com/",
            "is_required": "true",
            "sentiment": "no_sentiment",
            "data": {
                "options": [
                    {"value": "Very Satisfied", "sentiment": "positive"},
                    {"value": "Satisfied", "sentiment": "positive"},
                    {"value": "Not Satisfied", "sentiment": "negative"},
                    {"value": "Neutral", "sentiment": "neutral"}
                ]
            },
            "depends_on": [],
            "next": {
                "positive": "question_001",
                "negative": "question_002",
                "neutral": "question_003",
                "no_sentiment": "question123"
            }
        }
    }
}

cj_json = convert_survey_to_cj_json(survey_json)
import json
print(json.dumps(cj_json, indent=4))
