from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.cloudinary import upload_file_from_bytes
from app.schemas.schemas import StudentRegister, TeacherRegister, Login, Token
from app.services.auth_service import (
    register_student,
    register_teacher as register_teacher_service,
    login
)
from app.utils.auth import decode_token
from fastapi import UploadFile, File, Form


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/student")
def student_registration(student_data: StudentRegister, db: Session = Depends(get_db)):
    """Register a new student"""
    user = register_student(db, student_data)
    return {"message": "Student registered successfully", "user_id": user.id}


@router.post("/register/teacher")
async def register_teacher(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),

    experience: int = Form(...),
    subjects: str = Form(...),
    hourly_fee: int = Form(...),
    address: str = Form(...),

    aadhaar_file: UploadFile = File(...),
    voter_file: UploadFile = File(...),
    qualification_file: UploadFile = File(...),

    db: Session = Depends(get_db)
):
    aadhaar_url = upload_file_from_bytes(
        aadhaar_file.file.read(),
        aadhaar_file.filename,
        "teacher-documents"
    )

    voter_url = upload_file_from_bytes(
        voter_file.file.read(),
        voter_file.filename,
        "teacher-documents"
    )

    qualification_url = upload_file_from_bytes(
        qualification_file.file.read(),
        qualification_file.filename,
        "teacher-documents"
    )

    teacher_data = TeacherRegister(
        name=name,
        email=email,
        phone=phone,
        password=password,

        aadhaar_url=aadhaar_url,
        voter_id_url=voter_url,
        qualification_url=qualification_url,

        experience=experience,
        subjects=subjects,
        hourly_fee=hourly_fee,
        address=address
    )

    user = register_teacher_service(
        db,
        teacher_data
    )

    return {
        "message":
        "Teacher registered successfully. Please wait for admin verification.",
        "user_id": user.id
    }

@router.post("/login")
def user_login(login_data: Login, db: Session = Depends(get_db)):
    """Login user"""
    result = login(db, login_data)
    return Token(**result)


@router.post("/logout")
def user_logout():
    """Logout user (client-side token removal)"""
    return {"message": "Logged out successfully"}


@router.get("/verify-token")
def verify_token(token: str):
    """Verify JWT token"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"valid": True, "payload": payload}