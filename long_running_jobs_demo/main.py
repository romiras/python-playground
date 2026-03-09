from typing import Any
import logging
from fastapi import FastAPI, Form, BackgroundTasks
from contextlib import asynccontextmanager
from pydantic import BaseModel
from time import sleep
from datetime import datetime
from job_state import JobState
from models import db, SearchJob, new_search_job, find_search_job

# db is defined and owned by the models module; we just connect here.
db.connect()
db.create_tables([SearchJob])


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    # Closing DB connection
    db.close()


# logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI(lifespan=lifespan)


def search_stub(job_id):
    search_job = find_search_job(job_id=job_id)
    if search_job is None:
        return

    search_job.status = JobState.PROCESSING
    search_job.save()

    sleep(5) # emulate a delay

    logging.info(f"search_job: {search_job}")

    search_job.status = JobState.COMPLETED
    search_job.updated_at = datetime.now()
    search_job.data = {
        "query": search_job.query,
        "data": "foo" # emulate a processing that has updated this field
    }
    search_job.save()


@app.post("/api/v1/search", status_code=201)
async def search_request(background_tasks: BackgroundTasks, q: str = Form(...)):
    # create a record in DB
    search_job = new_search_job(
        query=q
    )

    # schedule a task to MQ
    background_tasks.add_task(search_stub, search_job.job_id)

    return {
        "job_id": search_job.job_id
    }


@app.get("/api/v1/search_results_polling")
async def search_results_polling(job_id: str):
    search_job = find_search_job(job_id=job_id)
    if search_job is None:
        return {
            "status": None,
            "reason": f"Job {job_id} not found",
            "data": None
        }

    return build_search_job_result(search_job)


def build_search_job_result(search_job: SearchJob) -> dict[str, Any]:
    logging.debug(f"status: {search_job.status}")
    if search_job.status == JobState.PENDING:
        return { 
            "status": JobState.PENDING,
            "reason": None,
            "data": None 
        }
    elif search_job.status == JobState.PROCESSING:
        return { 
            "status": JobState.PROCESSING,
            "reason": None,
            "data": None 
        }
    elif search_job.status == JobState.FAILED:
        return { 
            "status": JobState.FAILED,
            "reason": search_job.reason,
            "data": None 
        }

    return { 
        "status": JobState.COMPLETED,
        "reason": None,
        "data": search_job.data
    }
