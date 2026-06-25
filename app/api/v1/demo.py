from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import DemoRequestCreate, DemoRequestResponse
from app.models.models import DemoRequest, Student, Teacher
from app.utils.auth import decode_token

router = APIRouter(prefix="/demo", tags=["Demo Requests"])


def get_current_student(token: str = Header(...), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    student = db.query(Student).filter(Student.id == user_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


@router.post("/")
def request_demo(
    demo_data: DemoRequestCreate,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Request a demo class from a teacher"""
    teacher = db.query(Teacher).filter(Teacher.id == demo_data.teacher_id).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    demo = DemoRequest(
        student_id=current_student.id,
        teacher_id=demo_data.teacher_id,
        status="pending"
    )
    
    db.add(demo)
    db.commit()
    db.refresh(demo)
    
    return {"message": "Demo class requested successfully"}