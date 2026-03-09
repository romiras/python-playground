from peewee import *
from datetime import datetime
from job_state import JobState
from utils import random_hex_string

# SQLite database. Using a file instead of :memory: so threads can share data.
db = SqliteDatabase('app.db')

class BaseModel(Model):
    """All models inherit this to share the database connection."""
    class Meta:
        database = db

class SearchJob(BaseModel):
    job_id = TextField(unique=True, null=False)
    status = TextField(null=False)
    reason = TextField(null=True)
    updated_at = DateTimeField(null=False)
    query = TextField(null=False)
    data = TextField(null=True)


def new_search_job(query: str) -> SearchJob:
    return SearchJob.create(
        job_id=random_hex_string(6),
        status=JobState.PENDING,
        reason="",
        updated_at=datetime.now(),
        query=query,
    )

def find_search_job(job_id: str) -> SearchJob | None:
    return SearchJob.get_or_none(job_id=job_id)
