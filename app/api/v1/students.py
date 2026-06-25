from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.schemas.schemas import StudentProfile
from app.models.models import Student
from app.utils.auth import decode_token

router = APIRouter(prefix="/students", tags=["Students"])


def get_current_student(token: str = Header(...), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    student = db.query(Student).filter(Student.id == user_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


@router.get("/profile")
def get_student_profile(current_student: Student = Depends(get_current_student)):
    """Get current student profile"""
    return {
        "id": current_student.id,
        "name": current_student.name,
        "email": current_student.email,
        "phone": current_student.phone,
        "address": current_student.address,
        "latitude": current_student.latitude,
        "longitude": current_student.longitude
    }


@router.put("/profile")
def update_student_profile(
    profile_data: StudentProfile,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Update student profile"""
    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(current_student, field, value)
    
    db.commit()
    db.refresh(current_student)
    
    return {"message": "Profile updated successfully"}