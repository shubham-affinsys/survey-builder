from http.client import HTTPException
from robyn import Robyn,Headers,Response,Request,serve_file,html,WebSocket,WebSocketConnector,ALLOW_CORS
import models
from models import *
from log import logger
import json
from utils import generate_uuid, fetch_all_answers, fetch_survey,format_survey_data
from validator import validate_user_response,is_valid_uuid, is_valid_format_survey, validate_data_survey
from utils import fetch_users, create_survey_json_file,create_user_response
from auth import get_password_hash,BasicAuthHandler
from robyn.authentication import AuthenticationHandler, BearerGetter, Identity

app = Robyn(__file__)

@app.before_request()
def before_req(request):
    logger.debug(f"request recieved --> {request.method} : {request.url.path}  body : {request.body}")
    return request

@app.after_request()
def after_req(response):
    logger.debug(f"request completed --> status: {response.status_code} desc :{response.description}")
    return response


#  QUESTION FROM SURVEY CRAETED IN AUTO GEN
from extractor import get_all_questions
@app.get("/survey_questions/:survey_id")
def get_survey_questions(request):
    survey_id = request.path_params.get("survey_id",None)

    if survey_id is None:
        logger.error("Survey id was not provided")
        return {"error":"please provide survey_id"}
    
    questions = get_all_questions(survey_id=survey_id)
    logger.info(f"question fetched from db success for survey_id : {survey_id}")
    return questions

#  STORE RESPOMSES TO DB
@app.post("/suvrey_response")
def save_survey_response(request):
    try:
        data = request.json()
        logger.info(f"user response was saved {data}")
        return Response(status_code=200,headers={"Content-Type":"text/plain"},description="Response saved success")
    except Exception as e:
        logger.error(f"error wile saving survey response {e}")
        return Response(status_code=500,headers={"Content-Type":"text/plain"},description="Invalid data provided")




# ANSWERS
@app.get("/answers")
async def get_all_answers(request):
    tenant = request.query_params.get('tenant',None)
    user_id = request.query_params.get('user_id',None)
    survey_id = request.query_params.get('survey_id',None)
    sentiment = request.query_params.get('sentiment',None)
    question_id = request.query_params.get('question_id',None)
    

    try:
        with SessionLocal() as session:
            answers = await fetch_all_answers(
                                            session=session,
                                            tenant = tenant,
                                            survey_id=survey_id,
                                            user_id=user_id,
                                            sentiment=sentiment,
                                            question_id=question_id
                                        )

        if answers is None:
            logger.warning("no Answer found")
            return {"data":"Not Found"}
            
        logger.info("Data fetched by DB success")
        return {"data":answers}
            
    except Exception as e:
        logger.error(f"error while fetching all answers {e}")
        return{"error":"cannot fetch all answers"}


# User-RESPONSE
@app.post("/user-response")
async def create_response(request):
    try:
        data = request.json()

        is_validated = await validate_user_response(data)
        if not is_validated :
            return Response(status_code=400,headers={"Content-Type":"application/json"},description=b'{"error":"invalid format expecting a uuid"}')
        
        with SessionLocal() as session:
            survey = await fetch_survey(session=session,survey_id=data.get('survey_id'))

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
            response  = await create_user_response(data, session, survey, user, response_id)
            if response is None:
                logger.error("could not populate user reposne table")



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

            logger.info(f"user response {response_id} saved ")
            return {"data": f"user response {response_id} saved"}
    except Exception as e:
        logger.error(f"Error occured while saving UserResponse {e}")
        return Response(status_code=500,headers={"Content-Type":"application/json"},description=b'{"error":"cannot save user responses"}')


@app.get("/user-responses")
async def get_all_response():
    try:
        with SessionLocal() as session:
            responses = session.query(UserResponse).all()
            responses = [response.as_dict() for response in responses]
            logger.info("All responses fetched from DB")
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
            logger.info(f"response {record.get('response_id',None)} fetched from DB")
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

            surveys = [survey.as_dict() for survey in surveys]
            
            logger.info("all surveys fetched from DB")
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
            logger.info(f"survey {survey.get('survey_id',None)} fetched from DB")
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
            logger.error("Invalid survey ID format. Expected valid UUID.")
            return Response(status_code=400,headers={"Content-Type":"application/json"},description=b'{"error":"invalid format expecting a uuid"}')
            
        with SessionLocal() as session:
            result = session.query(Survey).filter(Survey.survey_id==id).first()
            survey=result.scalar_one_or_none()
            if not survey:
                logger.warning(f"survey does not exist with survey_id {id}")
                return Response(status_code=404,headers={"Content-Type":"application/json"},description=b'{"error":"survey does not exists"}')

            record = session.delete(survey)
            session.commit()
            logger.info(f"survey {id} deleted from DB")
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
        
        data = await format_survey_data(data)
        
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

        file_created = await create_survey_json_file(data)

        if not file_created:
            logger.error("json file was not cerated")

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
                return Response(status_code=409,headers=Headers({"Content-Type":"application/json"}),description=b'{"error":"username already exists"}')
            
            user_pass = data.get('password',None)
            if not user_pass:
                logger.warning("password filed is was not provided")
                return {"error":"password filed is was not provided"}
            
            hashed_password =  get_password_hash(user_pass)
            user = User(
                username=data.get('username', 'unknown'),
                mobile_no=data.get('mobile_no', None),
                email=data.get('email', None),
                hashed_password=hashed_password,
                created_at=naive_time
            )

            session.add(user)
            session.commit()
            session.refresh(user)

        logger.info("user created success")
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
    try:
        with SessionLocal() as session:
            users = await fetch_users(session)
        logger.info("all users fetched from db")
        return {"users": users}
    except Exception as e:
        logger.error(f"error while fetching all users : {e}")
        return Response(status_code=500,headers=Headers({"Content-Type":"application/json"}),description=b'{"error":"Internal Server Error"}')


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

#         logger.info("All users fetched from db")
#         return {"users": users}



@app.get("/")
async def index(request):
    return "Hello World!"

from auth import BasicAuthHandler, BearerGetter

# app.configure_authentication(BasicAuthHandler(token_getter=BearerGetter()))
import os


@app.get("/html")
async def htm(request: Request):
    try:
        auth = request.headers.get("Authorization")
        logger.info(f"request auth info : {auth}")

        if not auth:
            return Response(status=302, headers={'Location': '/auth/login'},description="Redirecting to Login")
        
    except Exception as e:
        logger.error(f"Error while authenticating user {e}")
        return Response(status=302, headers={'Location': '/login'})
    
    try:
        file_path = os.getcwd()+"/index.html"
        print(file_path)

        return serve_file(file_path)
        # return serve_file(file_path, file_name="my_html")

    except Exception as e:
        logger.error(f"error:{e}")
        return html("<h3>Error<h3>")


# serve a directory
app.serve_directory(
            route="/code_files",
            directory_path=os.path.join(os.getcwd()),
            index_file="index.html",
        )

from auth import authenticate_user

@app.post("users/register")
async def register_user(request):
    userv= request.json()
    with SessionLocal() as session:
        created_user = await create_user(request)
        return created_user

@app.post("/users/login")
async def login_user(request: Request):
    user = request.json()
    next_url = request.query_params.get("next", "/")  

    # Authenticate the user
    with SessionLocal() as session:
        token = await authenticate_user(session, **user)

    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"access_token": token}


@app.get("/users/me", auth_required=True)
async def get_current_user(request):
    user = request.identity.claims.get("user")
    logger.info(f"user info: {user}")
    return user

# from jinja2 import Environment, FileSystemLoader
# import os
# from robyn import Request, Response

# # Set up Jinja2 environment
# template_loader = FileSystemLoader(searchpath=os.getcwd() + '/svc/templates/')
# template_env = Environment(loader=template_loader)

# def render_template(template_name, **kwargs):
#     template = template_env.get_template(template_name)
#     return template.render(**kwargs)

from robyn.templating import JinjaTemplate
import pathlib

current_file_path = pathlib.Path(__file__).parent.resolve()
JINJA_TEMPLATE = JinjaTemplate(os.path.join(current_file_path, "templates"))

@app.get("/template_render")
def template_render(template_name: str, next_url: str = None):
    context = {"framework": "Robyn", "templating_engine": "Jinja2"}
    if next_url:
        context["next_url"] = next_url
    else:
        context["next_url"] = "/"

    template = JINJA_TEMPLATE.render_template(template_name=f"{template_name}", **context)
    return template

@app.get("/login")
async def login_page(request: Request):
    try:
        next_url = request.query_params.get("next", "/")   # redirect to / if next url is not found
        # login_page = template_render("login.html", next_url=next_url)
        login_page = template_render("login.html")
        return login_page
    except Exception as e:
        logger.error(f"Error serving login page: {e}")
        return Response(500, description="Error loading login page.", headers={"Content-type": "text/html"})


def sync_decorator_view():
    def get():
        return "Hello, world!"

    def post(request: Request):
        body = request.body
        return body

app.add_view("/sync/view/decorator", sync_decorator_view)




@app.post("/test_email")
async def test_email(request):
    # Set CORS headers
    response = Response("Thank you for your feedback!", status_code=200)
    response.headers["Access-Control-Allow-Origin"] = "*"  # Allow requests from all origins
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    # Parse the form data
    data = await request.json()
    print(f"user response is: {data}")
    
    return response

ALLOW_CORS(app, origins = ["http://localhost:5500"])
if __name__ == "__main__":
    # app.startup_handler(connect_db)
    # app.startup_handler(connect_db)
    # app.shutdown_handler(shutdown_db)
    
    # app.configure_authentication(BasicAuthHandler(token_getter=BearerGetter()))
    app.start(host="0.0.0.0",port=8080)
