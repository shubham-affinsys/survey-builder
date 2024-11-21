import uuid
from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, Column, String, DateTime, JSON, Integer, ForeignKey, Boolean
import sys
from log import logger

from sqlalchemy.future import select
import asyncio
load_dotenv()

Base = declarative_base()

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker




class Helper:
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

def generate_uuid():
    return str(uuid.uuid4())



class User(Base, Helper):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    username = Column(String, nullable=False)
    mobile_no = Column(String, nullable=True)
    email = Column(String, nullable=True)
    hashed_password = Column(String,nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    responses = relationship('UserResponse', back_populates='user')


class Survey(Base, Helper):
    __tablename__ = 'surveys'

    survey_id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    survey_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_by = Column(String, nullable=False)
    tenant = Column(String,nullable=False)

    questions = relationship('Question', back_populates='survey')
    responses = relationship('UserResponse', back_populates='survey')


class Question(Base, Helper):
    __tablename__ = 'questions'

    question_id = Column(String, primary_key=True, default=str(generate_uuid))
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.survey_id', ondelete='CASCADE'))
    question_text = Column(String, nullable=True)
    is_required = Column(Boolean, default=False)
    question_type = Column(String, nullable=False)
    sentiment = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    next_questions = Column(String, nullable=True)

    survey = relationship('Survey', back_populates='questions')
    answers = relationship('Answer', back_populates='question')


class UserResponse(Base, Helper):
    __tablename__ = 'responses'

    response_id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.survey_id', ondelete='CASCADE'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'))
    response_sentiment = Column(String, nullable=True)
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    time_taken = Column(Integer, nullable=True)
    no_of_questions_asked = Column(Integer, nullable=True)
    no_of_questions_answered = Column(Integer, nullable=True)
    tenant = Column(String,nullable=False)

    survey = relationship('Survey', back_populates='responses')
    user = relationship('User', back_populates='responses')
    answers = relationship('Answer', back_populates='response')


class Answer(Base, Helper):
    __tablename__ = 'answers'

    answer_id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    question_id = Column(String, ForeignKey('questions.question_id', ondelete='CASCADE'))
    response_id = Column(UUID(as_uuid=True), ForeignKey('responses.response_id', ondelete='CASCADE'))
    answer_text = Column(String, nullable=True)
    answer_sentiment = Column(String, nullable=True)
    answered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    question = relationship('Question', back_populates='answers')
    response = relationship('UserResponse', back_populates='answers')




# DB_URL = f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}?sslmode=require"
DB_URL = f"postgresql+psycopg2://{getenv('PGUSER')}:{getenv('PGPASSWORD')}@{getenv('PGHOST')}:{getenv('PGPORT')}/{getenv('POSTGRES_DB')}"

try:
    logger.info("creating engine...")
    engine = create_engine(DB_URL, pool_size=20, max_overflow=10)
    logger.info(f"engine: {engine}")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Base.metadata.drop_all(bind=engine)
    logger.info("engine created!!!")
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created!!!")

except Exception as e:
    logger.error(f"error cannot connect to DB {e}")


# DB_URL = f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"

# try:

#     print("creating engine...")
#     # engine = create_engine(getenv('POSTGRES_DB_URL'), pool_size=20, max_overflow=10)
#     engine = create_async_engine(DB_URL,pool_size=20,max_overflow=10)
#     print("engine created!!!")
    

#     print("creating session...")
#     SessionLocal = sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)
#     print("session created!!!")

#     async def async_create_all():
#         try:
#             print("Creating tables if they dont exist in DB...")
#             async with engine.begin() as conn:
#                 await conn.run_sync(Base.metadata.create_all)
#             print("Tables created in DB if they didnt exist !!!")
#             await engine.dispose()
#             print("engine disposed")
#         except Exception as e:
#             print(f"error while creating tables in db  : {e}")

#     asyncio.run(async_create_all())

# except Exception as e:
#     print(f"cannot connect to DB {e}")




















# # async def connect_db():
# #     print("creating session...")
# #     try:
# #         session = SessionLocal()
# #         await session.execute(select(User))
# #         print("session created!!!")
# #     except Exception as e:
# #         print(f"cannot create sesskion {e}")

# # from itertools import cycle

# # # Create engines for each database URL
# # engines = [create_async_engine(url, pool_size=10, max_overflow=20) for url in ["postgresql+asyncpg://shubh:9504@localhost:5432/survey_db"]]
# # SessionLocal = [async_sessionmaker(engine, expire_on_commit=False) for engine in engines]

# # Create a round-robin iterator
# # engine_cycle = cycle(SessionLocal)
# #     async with engines[0].begin() as conn:  # Use any engine; here we use the first.
# #         await conn.run_sync(Base.metadata.create_all)

# try:
#     # engine = create_engine(getenv('POSTGRES_DB_URL'), pool_size=20, max_overflow=10)
#     print("creating engine...")
#     # engine = create_async_engine(getenv('POSTGRES_DB_URL'))
#     engine = create_async_engine("postgresql+asyncpg://shubh:9504@postgres:5432/survey_db", pool_size=20, max_overflow=10)
#     print("engine created...")
#     # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     SessionLocal = sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)
#     # async def async_create_all():
#     #     # Use the engine in an async context to create tables
#     #     async with engine.begin() as conn:
#     #         await conn.run_sync(Base.metadata.create_all)

#     # # Run the async_create_all function
#     # asyncio.run(async_create_all())
#     # print("Database tables created successfully.")


# except Exception as e:
#     print(f"cannot connect to DB {e}")
#     sys.exit(0)



# # Base.metadata.drop_all(bind=engine)
# # Base.metadata.create_all(bind=next(engines))



