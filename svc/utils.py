from log import logger
import uuid
import json
from validator import  validate_data_survey
from sqlalchemy.future import select

# DATABASE QUERIES

#ANSWERS
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Answer, Survey, User, UserResponse, Question


async def fetch_all_answers(session: Session,
                           tenant=None,
                           survey_id=None,
                           user_id=None,
                           sentiment=None,
                           question_id=None,
                           limit=None,
                           offset=None):
    
    """
    fn makes query to DB to fetch answers based on parameters session is the only mandatory parameter
    return list of answers fitered on basis of fn params
    """
    try:
        # Build base query
        query = session.query(Answer)

        # Add filters dynamically
        # if tenant:
        #     query = query.filter(Answer.tenant == tenant)
        # if survey_id:
        #     query = query.filter(Answer.survey_id == survey_id)
        # if user_id:
        #     query = query.filter(Answer.user_id == user_id)
        if sentiment:
            query = query.filter(Answer.answer_sentiment == sentiment)
        if question_id:
            query = query.filter(Answer.question_id == question_id)

        # Add pagination if specified
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        # Execute query and fetch results
        data = query.all()

        if not data:
            logger.debug("No data found for query")
            return None

        # Convert to dict if needed
        data = [record.as_dict() for record in data]
        logger.debug("Data fetched from DB")
        return data

    except Exception as e:
        logger.error(f"Error while querying from DB: {e}")
        return None


# SURVEY
async def fetch_survey(session,survey_id):

    try:
        record = session.query(Survey).filter(Survey.survey_id==survey_id).first()

        if not record:
            logger.warning("no record found for query suvrey")
            return None
        
        logger.info("Data fetched from DB for survey")
        return record
    
    except Exception as e:
        logger.error(f"Error while fetching data from DB {e}")
        return None
    
async def create_user_response(data, session, survey, user, response_id):
    try:
        response = UserResponse(
                    survey_id = survey.survey_id,
                    user_id = user.user_id,
                    response_id=response_id,
                    response_sentiment=data.get('response_sentiment',None),
                    time_taken=data.get('time_taken',0),
                    no_of_questions_asked=data.get('questions_asked'),
                    no_of_questions_answered=data.get('questions_answered'),
                    tenant = data.get('tenant')
                )

        session.add(response)
        session.commit()
        session.refresh(response)
        return response
    except Exception as e:
        logger.error(f"error while creating user-resposne {e}")
        return None


async def format_survey_data(data):
    """
    request.json() fn is not able to format nested value and takes tem as string
    returns a json/dict
    """
    try:
        if isinstance(data.get('nodes'), str):
            data['nodes'] = json.loads(data['nodes'])

        if isinstance(data.get('questions'), str):
            data['questions'] = json.loads(data['questions'])

        if isinstance(data.get('theme_data'), str):
            data['theme_data'] = json.loads(data['theme_data'])

        if isinstance(data.get('total_questions'), str):
            data['total_questions'] = int(data['total_questions'])
        
        is_valid = await validate_data_survey(data)

        if not is_valid:
            logger.warning("data is not in correct format or fields are missing")
            return {"error":"data is not in correct format or some fields are missing"}
        
        return data
    except Exception as e:
        logger.error(f"error while formating survey data: {e}")    
        return None
    
import os
SURVEYS_FOLDER =  os.path.join(os.getcwd(), "surveys")

async def create_survey_json_file(data):
    survey_title = data.get("survey_title", "default")
    file_name = f"survey_{survey_title}.json"

    os.makedirs(SURVEYS_FOLDER, exist_ok=True)
    file_path = os.path.join(SURVEYS_FOLDER, file_name)

    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        logger.info(f"{file_name} file created success")
        return True
    
    except Exception as e:
        logger.error("error while creating  survey json file")
        return False


# USERS
async def fetch_users(session:Session):
    users = session.query(User).all()
    users = [user.as_dict() for user in users]
    return users

async def fetch_user(session:Session,username:str):
    try:
        record = session.query(User).filter(User.username==username).first()
        if record:
            user = record.as_dict()
            return user
        return None
    except Exception as e:
        logger.error(f"Cannot fetch user form DB {e}")
        return None

# MISCS
def generate_uuid():
    return str(uuid.uuid4())



async def send_message(channel,data):
    logger.info("Predaring Payload to send message...")
    try:
        payload = await create_message_payload(channel,data)
        logger.info(f"Payload created: {payload}")
        
        logger.info("sending message to channel..")

        logger.info("messsage sent")
        return True
    except Exception as e:
        logger.error(f"Error while creating payload : {e}")
        return False


async def create_message_payload(platform, content):
    """
    Create a payload for WhatsApp, Email, or SMS messaging.

    Args:
        platform (str): The platform to send the message ('whatsapp', 'email', 'sms').
        content (dict): The content dictionary with the required keys:
                        - WhatsApp: {'to': str, 'message': str}
                        - Email: {'to': str, 'subject': str, 'message': str, 'from_email': str}
                        - SMS: {'to': str, 'message': str, 'from_number': str}

    Returns:
        dict: The payload formatted for the specified platform.
    """
    if platform == "whatsapp":
        return {
            "messaging_product": "whatsapp",
            "to": content["to"],
            "type": "text",
            "text": {"body": content["message"]},
        }
    elif platform == "email":
        return {
            "personalizations": [
                {
                    "to": [{"email": content["to"]}],
                    "subject": content["subject"],
                }
            ],
            "from": {"email": content["from_email"]},
            "content": [
                {
                    "type": "text/plain",
                    "value": content["message"],
                }
            ],
        }
    elif platform == "sms":
        return {
            "From": content["from_number"],
            "To": content["to"],
            "Body": content["message"],
        }
    else:
        raise ValueError("Unsupported platform. Choose 'whatsapp', 'email', or 'sms'.")

# import asyncio

# channel = "whatsapp"
# data = {"to": "1234567890", "message": "Hello from WhatsApp!"}

# asyncio.run(send_message(channel=channel,data=data))