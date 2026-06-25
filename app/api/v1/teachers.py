from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.schemas.schemas import TeacherProfile, TeacherResponse, NearbySearch
from app.models.models import Teacher, Review
from app.utils.auth import decode_token
from app.utils.cloudinary import upload_file_from_bytes
from app.services.teacher_service import get_all_teachers, get_teacher_by_id, update_teacher_profile, get_teachers_nearby
import uuid

router = APIRouter(prefix="/teachers", tags=["Teachers"])


def get_current_teacher(token: str = Header(...), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    teacher = db.query(Teacher).filter(Teacher.id == user_id).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    return teacher


@router.get("/")
def get_teachers(db: Session = Depends(get_db)):
    """Get all verified teachers"""
    return get_all_teachers(db)


@router.get("/nearby")
def get_nearby_teachers(
    lat: float,
    lng: float,
    radius: float = 5,
    db: Session = Depends(get_db)
):
    """Get teachers within radius kilometers"""
    return get_teachers_nearby(db, lat, lng, radius)


@router.get("/{teacher_id}")
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """Get teacher by ID"""
    return get_teacher_by_id(db, teacher_id)

@router.get("/profile")
def get_teacher_profile(
    current_teacher: Teacher = Depends(get_current_teacher)
):
    """Get current teacher profile"""

    return {
        "id": current_teacher.id,
        "name": current_teacher.name,
        "email": current_teacher.email,
        "phone": current_teacher.phone,
        "subjects": current_teacher.subjects,
        "experience": current_teacher.experience,
        "hourly_fee": current_teacher.hourly_fee,
        "address": current_teacher.address,
        "profile_photo_url": current_teacher.profile_photo_url,
        "is_verified": current_teacher.is_verified
    }

@router.put("/profile")
def update_profile(
    profile_data: TeacherProfile,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update teacher profile"""
    return update_teacher_profile(db, current_teacher.id, profile_data)


@router.post("/upload-profile-photo")
def upload_profile_photo(
    file: UploadFile = File(...),
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Upload teacher profile photo"""
    try:
        file_bytes = file.file.read()
        filename = f"{uuid.uuid4()}_{file.filename}"
        url = upload_file_from_bytes(file_bytes, filename, "teacher-profiles")
        
        current_teacher.profile_photo_url = url
        db.commit()
        
        return {"message": "Profile photo uploaded successfully", "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/profile")
def update_teacher_profile(
    profile_data: TeacherProfile,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update teacher profile"""
    return update_teacher_profile(db, current_teacher.id, profile_data)


@router.post("/upload-profile-photo")
def upload_profile_photo(
    file: UploadFile = File(...),
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Upload teacher profile photo"""
    try:
        file_bytes = file.file.read()
        filename = f"{uuid.uuid4()}_{file.filename}"
        url = upload_file_from_bytes(file_bytes, filename, "teacher-profiles")
        
        current_teacher.profile_photo_url = url
        db.commit()
        
        return {"message": "Profile photo uploaded successfully", "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))