from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, func
from dotenv import load_dotenv
from os import getenv
import asyncio

# Load environment variables
load_dotenv()

# Database configuration
DB_URL1 = f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
enginea = create_async_engine(DB_URL1, pool_size=20, max_overflow=10)
SessionA = async_sessionmaker(bind=enginea, expire_on_commit=False)
from models import Survey, User, UserResponse

# Define analytics functions
async def get_total_responses_per_survey(session: AsyncSession):
    query = (
        select(Survey.title, func.count(UserResponse.response_id).label("response_count"))
        .join(UserResponse, Survey.survey_id == UserResponse.survey_id)
        .group_by(Survey.survey_id)
    )
    result = await session.execute(query)
    return result.all()

async def get_average_time_per_survey(session: AsyncSession):
    query = (
        select(Survey.title, func.avg(UserResponse.time_taken).label("average_time"))
        .join(UserResponse, Survey.survey_id == UserResponse.survey_id)
        .group_by(Survey.survey_id)
    )
    result = await session.execute(query)
    return result.all()

async def get_user_engagement(session: AsyncSession):
    query = (
        select(User.username, func.count(UserResponse.response_id).label("response_count"))
        .join(UserResponse, User.user_id == UserResponse.user_id)
        .group_by(User.user_id)
    )
    result = await session.execute(query)
    return result.all()

async def get_sentiment_breakdown(session: AsyncSession, survey_id: str):
    query = (
        select(UserResponse.response_sentiment, func.count(UserResponse.response_id).label("count"))
        .where(UserResponse.survey_id == survey_id)
        .group_by(UserResponse.response_sentiment)
    )
    result = await session.execute(query)
    return result.all()

async def get_responses_over_time(session: AsyncSession, survey_id: str):
    query = (
        select(
            func.date_trunc('day', UserResponse.submitted_at).label('date'),
            func.count(UserResponse.response_id).label('response_count')
        )
        .where(UserResponse.survey_id == survey_id)
        .group_by('date')
        .order_by('date')
    )
    result = await session.execute(query)
    return result.all()

# Main analytics runner
async def run_analytics():
    async with SessionA() as session:
        try:
            total_responses = await get_total_responses_per_survey(session)
            print("Total Responses Per Survey:", total_responses)

            avg_time = await get_average_time_per_survey(session)
            print("Average Time Per Survey:", avg_time)

            user_engagement = await get_user_engagement(session)
            print("User Engagement:", user_engagement)

            survey_id = "2797ea1b-6032-4a6a-8911-0cca37161c63"
            sentiment_breakdown = await get_sentiment_breakdown(session, survey_id)
            print(f"Sentiment Breakdown for Survey {survey_id}:", sentiment_breakdown)

            responses_over_time = await get_responses_over_time(session, survey_id)
            print(f"Responses Over Time for Survey {survey_id}:", responses_over_time)
        except Exception as e:
            print(f"An error occurred during analytics execution: {e}")



if __name__ == "__main__":
    try:
        asyncio.run(run_analytics())
    except Exception as e:
        print(f"error while running analytics : {e}")
