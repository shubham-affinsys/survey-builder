from log import logger
import uuid



## ANSWER VALIDATORS
async def validate_user_response(data):
    """
    function validate_user_response  validates:
    1. The format of user_id and survey_id is uuid
    2. All the required fileds are present in the data
    """
    logger.debug("validating user response...")
    # check if user_id is uuid
    if not is_valid_uuid(data.get('user_id')):
        logger.error("Invalid user_id  format. Expected a valid UUID.")
        return False
    
    # check if survey_id is uuid
    if not is_valid_uuid(data.get('survey_id')):
        logger.error("Invalid survey_id format. Expected a valid UUID.")
        return False           
    logger.debug("user response  is valid")
    return True



# VALIDATORS SURVEY

async def is_valid_format_survey(data):
    logger.debug("validating survey data format...")
    required_fields = {
        "survey_title": str,
        # "survey_id": str,
        "description": str,
        "total_questions": str,
        "nodes": str,
        "questions": str,
        "created_at": str,
        "tenant": str,
        "created_by": str,
        "theme_data": str,
    }

    # First-level validation
    for field, field_type in required_fields.items():
        if field not in data or not isinstance(data[field], field_type):
            logger.error(f"{field} fields are missing")
            return False
        
    logger.info("survey data is valid no fields missing")
    return True


async def validate_data_survey(data):
    logger.debug("validating survey data")

    # Validate theme_data fields
    if "logo" in data["theme_data"] and not isinstance(data["theme_data"]["logo"], str):
        return False
    if "colors" in data["theme_data"] and not isinstance(data["theme_data"]["colors"], str):
        return False

    # Validate nodes structure
    for node_id, node in data["nodes"].items():
        node_required_fields = {
            "id": str,
            "type": str,
            "name": str,
            "width": int,
            "height": int,
            "position": dict,
            "previous": list,
            "next": list,
        }
        
        for field, field_type in node_required_fields.items():
            if field not in node or not isinstance(node[field], field_type):
                return False

        # Validate position in each node
        if "x" not in node["position"] or "y" not in node["position"]:
            return False
        if not isinstance(node["position"]["x"], int) or not isinstance(node["position"]["y"], int):
            return False

    # Validate questions structure
    for question_id, question in data["questions"].items():
        question_required_fields = {
            "type": str,
            "text": str,
            "description": str,
            "is_required": str,
            "sentiment": str,
            "data": dict,
            "depends_on": list,
            "next": dict,
        }
        
        for field, field_type in question_required_fields.items():
            if field not in question or not isinstance(question[field], field_type):
                return False

        # Validate data field in each question
        if question["type"] == "mcq" and "options" in question["data"]:
            for option in question["data"]["options"]:
                if not isinstance(option.get("value"), str) or not isinstance(option.get("sentiment"), str):
                    return False
        elif question["type"] == "text_feild" and "input" in question["data"]:
            input_field = question["data"]["input"]
            if not isinstance(input_field.get("value"), str) or not isinstance(input_field.get("sentiment"), str):
                return False
            
    return True

# MISC
def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except:
        return False
    