import uuid
from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, Column, String, DateTime, JSON, Integer, ForeignKey, Boolean
from utils import generate_uuid

load_dotenv()

Base = declarative_base()


engine = create_engine(getenv('POSTGRES_DB_URL'), pool_size=20, max_overflow=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Helper:
    async def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}




class User(Base, Helper):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    username = Column(String, nullable=False)
    mobile_no = Column(String, nullable=True)
    email = Column(String, nullable=True)
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

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
