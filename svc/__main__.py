from robyn import Robyn,Headers,Response
import models
from models import *
from log import logger
import json
from utils import generate_uuid,is_valid_uuid,is_valid_format_survey,validate_data_survey

app = Robyn(__file__)

# @app.before_request()
# def before_req(request):
#     print("request recieved")
#     return request

# @app.after_request()
# def after_req(response):
#     print("request completed")
#     return response



# ANSWERS

@app.get("/answers")
async def get_all_answers():
    try:
        with SessionLocal() as session:
            answers = session.query(Answer).all()
            answers = [await answer.as_dict() for answer in answers]
            return {"data":answers}
    except Exception as e:
        logger.error(f"error while fetching all answers {e}")
        return{"error":"cannot fetch all answers"}



# RESPONSE


@app.post("/user-response")
async def create_response(request):
    try:
        data = request.json()
        with SessionLocal() as session:

            if not is_valid_uuid(data.get('user_id')):
                logger.error("Invalid user_id  format. Expected a valid UUID.")
                return Response(status_code=400,headers={"Content-Type":"application/json"},description=b'{"error":"invalid format for user_id expecting a uuid"}')
            if not is_valid_uuid(data.get('survey_id')):
                logger.error("Invalid survey_id format. Expected a valid UUID.")
                return Response(status_code=400,headers={"Content-Type":"application/json"},description=b'{"error":"invalid format for survey_id expecting a uuid"}')
           

            # check if surevy id  is valid
            survey = session.query(Survey).filter(Survey.survey_id==data.get('survey_id')).first()
            if not survey:
                logger.error("error survey_id does not esist in DB")
                return {"error":"survey_id is invalid"}
            
            # check if user_id is valid
            user = session.query(User).filter(User.user_id==data['user_id']).first()
            if not user:
                logger.error("error user_id does not esist in DB")
                return {"error":"user_id is invalid"}
            
            # create respose
            response_id = generate_uuid()
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


            # populate questions table
            if isinstance(data.get('responses'),str):
                data['responses'] = json.loads(data['responses'])
            
            questions = []
            for response_data in data.get('responses', []):
                existing_question = session.query(Question).filter(
                    Question.question_id == response_data['question_id'],
                    Question.survey_id == survey.survey_id
                ).first()
                
                # Only add question if it doesn't already exist
                if not existing_question:
                    question = Question(
                        question_id=response_data['question_id'],
                        survey_id=survey.survey_id,
                        question_text=response_data['text'],
                        is_required=response_data['is_required'].lower() == 'true',
                        question_type=response_data['type'],
                        sentiment=response_data['sentiment'],
                        next_questions=response_data['next'].strip('"') if response_data['next'] else None
                    )
                    questions.append(question)

            # Add all non-duplicate questions and commit them to the database
            if questions:
                session.add_all(questions)
                session.commit()

            # populate answers table
            answers = [
                Answer(
                    question_id=response_data['question_id'],
                    response_id=response_id,
                    answer_text=response_data['value'],
                    answer_sentiment= response_data['sentiment'],

                ) for response_data in data.get('responses', [])
            ]

            session.add_all(answers)
            session.commit()



            logger.debug(f"user response {response_id} saved ")
            return {"data": f"user response {response_id} saved"}
    except Exception as e:
        logger.error(f"Error occured while saving UserResponse {e}")
        return Response(status_code=500,headers={"Content-Type":"application/json"},description=b'{"error":"cannot save user responses"}')



@app.get("/user-responses")
async def get_all_response():
    try:
        with SessionLocal() as session:
            responses = session.query(UserResponse).all()
            responses = [await response.as_dict() for response in responses]
            logger.debug("All responses fetched from DB")
            return {"data": responses}
    except Exception as e:
        logger.error(f"Error occured while fetching all UserResponses {e}")
        return Response(status_code=500,headers={"Content-Type":"application/json"},description=b'{"error":"cannot fetch user responses"}')


@app.get("/user-response")
async def get_response(request):
    try:
        id = request.query_params.get('response_id')

        if not is_valid_uuid(id):
            logger.error("Invalid reponse ID format. Expected a valid UUID.")
            return Response(status_code=400,headers={"Content-Type":"application/json"},description=b'{"error":"invalid format expecting a uuid"}')
            
        with SessionLocal() as session:
            record = session.query(UserResponse).filter(UserResponse.response_id==id).first()
            if not record:
                logger.warning(f"survey does not exist with response_id {id}")
                return Response(status_code=404,headers={"Content-Type":"application/json"},description=b'{"error":"response does not exist"}')

            record =await record.as_dict()
            logger.debug(f"response {record.get('response_id',None)} fetched from DB")
            return {"data": record}

    except Exception as e:
        logger.error(f"Error occured while fetching survey {e}")
        return Response(status_code=500,headers={"Content-Type":"application/json"},description=b'{"error":"cannot fetch survey"}')



# SURVEY
@app.get("/surveys")
async def get_all_surveys():
    try:
        with SessionLocal() as session:
            surveys = session.query(Survey).all()

            surveys = [await survey.as_dict() for survey in surveys]
            
            logger.debug("all surveys fetched from DB")
            return {"data": surveys}
    except Exception as e:
        logger.error(f"Error occured while fetching all surveys {e}")
        return Response(status_code=500,headers={"Content-Type":"application/json"},description=b'{"error":"cannot fetch surveys"}')


@app.get("/survey")
async def get_survey(request):
    try:
        id = request.query_params.get('survey_id')

        if not is_valid_uuid(id):
            logger.error("Invalid survey ID format. Expected a valid UUID.")
            return Response(status_code=400,headers={"Content-Type":"application/json"},description=b'{"error":"invalid format expecting a uuid"}')
            
        with SessionLocal() as session:
            survey = session.query(Survey).filter(Survey.survey_id==id).first()
            if not survey:
                logger.warning(f"survey does not exist with survey_id {id}")
                return Response(status_code=404,headers={"Content-Type":"application/json"},description=b'{"error":"survey does not exists"}')

            survey =await survey.as_dict()
            logger.debug(f"survey {survey.get('survey_id',None)} fetched from DB")
            return {"data": survey}

    except Exception as e:
        logger.error(f"Error occured while fetching survey {e}")
        return Response(status_code=500,headers={"Content-Type":"application/json"},description=b'{"error":"cannot fetch survey"}')


@app.delete("/survey")
async def delete_survey(request):
    try:
        id = request.query_params.get('survey_id',None)
        if not id:
            logger.warning("survey_id was not given")
            return Response(status_code=400,headers={"Content-Type":"application/json"},description=b'{"error":"survey_id is not provided"}')


        if not is_valid_uuid(id):
            logger.error("Invalid survey ID format. Expected a valid UUID.")
            return Response(status_code=400,headers={"Content-Type":"application/json"},description=b'{"error":"invalid format expecting a uuid"}')
            
        with SessionLocal() as session:
            result = session.query(Survey).filter(Survey.survey_id==id).first()
            survey=result.scalar_one_or_none()
            if not survey:
                logger.warning(f"survey does not exist with survey_id {id}")
                return Response(status_code=404,headers={"Content-Type":"application/json"},description=b'{"error":"survey does not exists"}')

            record = session.delete(survey)
            session.commit()
            logger.debug(f"survey {id} deleted from DB")
            return {"data":f"survey {id} deleted success"}

    except Exception as e:
        logger.error(f"Error occured while fetching survey {e}")
        return Response(status_code=500,headers={"Content-Type":"application/json"},description=b'{"error":"cannot delete survey"}')


@app.post("/create-survey")
async def create_survey(request):
    try:
        data = request.json()
        is_valid_format = await is_valid_format_survey(data)
        if not is_valid_format :
            logger.warning("fields are missing")
            return {"error":"fields are missing"}

        if isinstance(data.get('nodes'), str):
            data['nodes'] = json.loads(data['nodes'])

        if isinstance(data.get('questions'), str):
            data['questions'] = json.loads(data['questions'])

        if isinstance(data.get('theme_data'), str):
            data['theme_data'] = json.loads(data['theme_data'])

        if isinstance(data.get('total_questions'), str):
            data['total_questions'] = int(data['total_questions'])

        is_validated = await validate_data_survey(data)

        if not is_validated:
            logger.warning("data is not in correct format or fields are missing")
            return {"error":"data is not in correct format or some fields are missing"}

        with SessionLocal() as session:
            existing_survey = session.query(Survey).filter(Survey.title == data['survey_title']).first()
            if existing_survey:
                logger.warning("survey title  already exist")
                return {"error": "survey title already exists"}
            
            survey_id = generate_uuid()
            data['survey_id'] = survey_id
            new_survey = Survey(
                survey_id= survey_id,
                survey_data=data,
                title = data.get('survey_title'),
                description = data.get('description'),
                created_by =data.get('created_by'),
                tenant = data.get('tenant')
            )
            session.add(new_survey)
            session.commit()
            session.refresh(new_survey)
        logger.info(f"survey created success id {survey_id}")
        return {"data":f"survey created success {survey_id}"}

    except Exception as e:
        logger.error(f"error while creating user: {e}")
        return Response(status_code=500,headers={"Content-Type":"application/json"},description=b'{"error":"cannot create survey"}')


from datetime import datetime,timezone
current_time = datetime.now(timezone.utc)

# Convert to naive datetime (remove timezone)
naive_time = current_time.replace(tzinfo=None)



@app.post("/create-user")
async def create_user(request):
    try:
        data = request.json()
        with SessionLocal() as session:
            # Check if user already exists
            # result = await session.execute(select(User).filter(User.username == data.get('username')))
            # existing_user = result.scalar_one_or_none()

            existing_user = session.query(User).filter(User.username == data.get('username')).first()
            if existing_user:
                logger.warning("username already exists")
                return Response(status_code=409,headers=Headers({"Content-Type":"application/json"}),description=b'{"error":"user already exists"}')

            # Create new user
            user = User(
                username=data.get('username', 'unknown'),
                mobile_no=data.get('mobile_no', None),
                email=data.get('email', None),
                created_at=naive_time
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        logger.debug("user created success")
        return {"data": "user created successfully"}

    except Exception as e:
        logger.error(f"error occured : {e}")
        headers = Headers({"error": "Internal server error"})
        return Response(status_code=500,headers=Headers({"Content-Type":"application/json"}),description=b'{"error":"Internal Server Error"}')


from sqlalchemy.future import select


# SYNC
# create a route to fetch all users
@app.get("/users")
async def get_users():
    with SessionLocal() as session:
        users = session.query(User).all()
        users = [await user.as_dict() for user in users]
        logger.debug("all users fetched from db")
        return {"users": users}

# ASYNC
# @app.get("/users")
# async def get_users():
#     async with SessionLocal() as session:
#     # async_session = next(engine_cycle)
#     # async with async_session() as session:
#         result = await session.execute(select(User))
#         users = result.scalars().all()  # Collect all user objects

#         # Convert each user to a dictionary, with UUID fields as strings if needed
#         users = [
#             {
#                 **await user.as_dict(),
#                 "user_id": str(user.user_id)
#             }
#             for user in users
#         ]

#         logger.debug("All users fetched from db")
#         return {"users": users}



@app.get("/")
async def index():
    return "Hello World!"


if __name__ == "__main__":
    # app.startup_handler(connect_db)
    # app.startup_handler(connect_db)
    # app.shutdown_handler(shutdown_db)
    
    app.start(port=8080)


