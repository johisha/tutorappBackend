from sqlalchemy.orm import Session
from app.models.models import Student, Teacher
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.schemas.schemas import StudentRegister, TeacherRegister, Login
from fastapi import HTTPException, status


def register_student(db: Session, student_data: StudentRegister):
    # Check if email exists
    if db.query(Student).filter(Student.email == student_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create student
    student = Student(
        name=student_data.name,
        email=student_data.email,
        phone=student_data.phone,
        password_hash=get_password_hash(student_data.password),
        address=student_data.address,
        latitude=student_data.latitude,
        longitude=student_data.longitude
    )
    
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return student


def register_teacher(db: Session, teacher_data: TeacherRegister):
    # Check if email exists
    if db.query(Teacher).filter(Teacher.email == teacher_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create teacher (not verified by default)
    teacher = Teacher(
        name=teacher_data.name,
        email=teacher_data.email,
        phone=teacher_data.phone,
        password_hash=get_password_hash(teacher_data.password),
        aadhaar_url=teacher_data.aadhaar_url,
        voter_id_url=teacher_data.voter_id_url,
        qualification_url=teacher_data.qualification_url,
        experience=teacher_data.experience,
        subjects=teacher_data.subjects,
        hourly_fee=teacher_data.hourly_fee,
        address=teacher_data.address,
        latitude=teacher_data.latitude,
        longitude=teacher_data.longitude,
        is_verified=False
    )
    
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    
    return teacher


def login(db: Session, login_data: Login):
    print("LOGIN REQUEST:", login_data.dict())
    if (
        login_data.email == "admin@gmail.com"
        and login_data.password == "admin123"
        and login_data.role == "admin"
    ):
        token = create_access_token(
            data={
                "sub": "0",
                "email": "admin@gmail.com"
            },
            role="admin"
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "admin",
            "user_id": 0
        }
    if login_data.role == "student":
        user = db.query(Student).filter(Student.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    elif login_data.role == "teacher":
        user = db.query(Teacher).filter(Teacher.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_AUTHORIZED,
                detail="Invalid email or password"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        role=login_data.role
    )
    
    return {"access_token": token, "token_type": "bearer", "role": login_data.role, "user_id": user.id}