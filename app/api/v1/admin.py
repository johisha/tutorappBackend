from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Teacher, Student
from app.utils.auth import decode_token
from app.schemas.schemas import PendingTeacherResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_current_admin(token: str = Header(...)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return payload


@router.get("/pending-teachers")
def get_pending_teachers(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """Get all teachers pending verification"""
    teachers = db.query(Teacher).filter(Teacher.is_verified == False).all()
    
    result = []
    for teacher in teachers:
        result.append({
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "phone": teacher.phone,
            "experience": teacher.experience,
            "subjects": teacher.subjects,
            "hourly_fee": teacher.hourly_fee,
            "aadhaar_url": teacher.aadhaar_url,
            "voter_id_url": teacher.voter_id_url,
            "qualification_url": teacher.qualification_url,
            "created_at": teacher.created_at
        })
    
    return result

@router.get("/all-teachers")
def get_all_teachers(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Get all verified teachers"""

    teachers = (
        db.query(Teacher)
        .filter(Teacher.is_verified == True)
        .all()
    )

    result = []

    for teacher in teachers:
        result.append({
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "phone": teacher.phone,
            "subjects": teacher.subjects,
            "experience": teacher.experience,
            "hourly_fee": teacher.hourly_fee,
            "created_at": teacher.created_at,
            "is_verified": teacher.is_verified
        })

    return result

@router.get("/all-students")
def get_all_students(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Get all registered students"""

    students = db.query(Student).all()

    result = []

    for student in students:
        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "phone": student.phone,
            "address": student.address,
            "created_at": student.created_at
        })

    return result


@router.post("/approve-teacher/{teacher_id}")
def approve_teacher(teacher_id: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """Approve a teacher"""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher.is_verified = True
    db.commit()
    
    return {"message": "Teacher approved successfully"}


@router.post("/reject-teacher/{teacher_id}")
def reject_teacher(teacher_id: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """Reject a teacher"""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    db.delete(teacher)
    db.commit()
    
    return {"message": "Teacher rejected and removed"}


@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """Get platform analytics"""
    total_students = db.query(Student).count()
    total_teachers = db.query(Teacher).filter(Teacher.is_verified == True).count()
    pending_teachers = db.query(Teacher).filter(Teacher.is_verified == False).count()
    
    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "pending_teachers": pending_teachers,
        "active_users": total_students + total_teachers
    }