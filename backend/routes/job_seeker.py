from fastapi import APIRouter, HTTPException, UploadFile, File
from bson import ObjectId
from utils.db import db
router = APIRouter()
@router.post("/upload_resume")
async def upload_resume(user_id: str, resume: UploadFile = File(...)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    content = await resume.read()
    filename = f"{user_id}_resume.pdf"
    
    with open(f"resumes/{filename}", "wb") as file:
        file.write(content)

    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"resume": filename}})
    
    return {"message": "Resume uploaded successfully", "filename": filename}


@router.get("/search_jobs")
async def search_jobs(skill: str = None, location: str = None, title: str = None):
    """
    Retrieve a list of job postings filtered by skill, location, or title.
    """
    query = {}
    if skill:
        query["skills"] = {"$regex": skill, "$options": "i"} 
        query["location"] = {"$regex": location, "$options": "i"}  
    if title:
        query["title"] = {"$regex": title, "$options": "i"} 

    jobs = list(db.jobs.find(query).limit(100))

    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found matching the criteria")
    for job in jobs:
        job["_id"] = str(job["_id"])

    return {"jobs": jobs}

@router.get("/apply")
async def apply_for_job(job_id: str):
    print(job_id)
    user =  db.jobs.find_one({"job_id": job_id})
    application = {
        "job_id": job_id,
    }
    db.applications.insert_one(application)

    return {"message": "Application submitted successfully"}

@router.get("/applications")
async def get_applications():
    applications = list(db.applications.find({}, {"_id": 0}))
    
    return {"applications": applications}


