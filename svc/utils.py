from log import logger
import uuid
import json
from validator import  validate_data_survey
from sqlalchemy.future import select

# DATABASE QUERIES

#ANSWERS
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Answer

async def fetch_all_answers(session: Session,
                           tenant=None,
                           survey_id=None,
                           user_id=None,
                           sentiment=None,
                           question_id=None,
                           limit=None,
                           offset=None):
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
        data = [await record.as_dict() for record in data]
        logger.debug("Data fetched from DB")
        return data

    except Exception as e:
        logger.error(f"Error while querying from DB: {e}")
        return None


# SURVEY
async def fetch_survey(session,survey_id):
    from models import Survey

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


async def format_survey_data(data):
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


# MISCS
def generate_uuid():
    return str(uuid.uuid4())

