from fastapi import APIRouter, HTTPException, Depends
from models.schemas import Job
from utils.db import db
from utils.security import verify_password
from bson import ObjectId
from fastapi.responses import JSONResponse
import uuid

router = APIRouter()
@router.post("/post_job")
async def post_job(job: Job):
    job_data = job.__dict__
    print(job_data)
    unique_id = str(uuid.uuid1())
    print(unique_id) 
    data = {
            "title": job_data["title"],
            "description": job_data["description"],
            "skills": job_data["skills"],
            "salary": job_data["salary"],
            "location": job_data["location"],
            "job_id":unique_id,
            }
    db.jobs.insert_one(data)
    return {"message": "Job posted successfully"}

@router.put("/edit_job/{job_id}")
async def edit_job(job_id: str, job: Job):
    result =  db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": job.__dict__})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job updated successfully"}

@router.get("/jobs", response_model=Job)
async def get_jobs():
    jobs = list(db.jobs.find({}, {"_id": 0}))  # Exclude `_id` for simplicity in the frontend
    print(jobs)
    return JSONResponse(content=jobs)

