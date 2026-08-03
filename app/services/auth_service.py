from sqlalchemy.orm import Session
from app.models.models import Student, Teacher, Admin
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.schemas.schemas import StudentRegister, TeacherRegister, Login
from fastapi import HTTPException, status
import time
from sqlalchemy import text


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


# 

def login(db: Session, login_data: Login):
    total_start = time.time()
    print("LOGIN REQUEST:", login_data.dict())

    if login_data.role == "admin":
        admin = db.query(Admin).filter(Admin.email == login_data.email).first()

        print("ADMIN FOUND:", admin)

        if admin:
            print("EMAIL FROM DB:", admin.email)
            print("HASH FROM DB:", admin.password_hash)
            print("PASSWORD MATCH:", verify_password(login_data.password, admin.password_hash))

        if not admin or not verify_password(login_data.password, admin.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin email or password"
            )

        token = create_access_token(
            data={
                "sub": str(admin.id),
                "email": admin.email
            },
            role="admin"
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "admin",
            "user_id": admin.id
        }

#     elif login_data.role == "student":

#         start = time.time()
#         # user = db.query(Student).filter(Student.email == login_data.email).first()
        

#         start = time.time()

#         result = db.execute(
#         text("SELECT * FROM students WHERE email = :email LIMIT 1"),
#         {"email": login_data.email}
# )

#         user = result.first()

#         print("Raw SQL Time:", time.time() - start)
#         print("Student DB Query Time:", time.time() - start)

#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid email or password"
#             )

#         start = time.time()
#         password_ok = verify_password(login_data.password, user.password_hash)
#         print("Student Password Verify Time:", time.time() - start)


    elif login_data.role == "student":

         start = time.time()
         db.execute(text("SELECT 1"))
         print("SELECT 1 Time:", time.time() - start)

         start = time.time()
         user = db.query(Student).filter(Student.email == login_data.email).first()
         print("Student DB Query Time:", time.time() - start)

         if not user:
            raise HTTPException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Invalid email or password"
        )

         start = time.time()
         password_ok = verify_password(login_data.password, user.password_hash)
         print("Student Password Verify Time:", time.time() - start)
         if not password_ok:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

    elif login_data.role == "teacher":

        start = time.time()
        user = db.query(Teacher).filter(Teacher.email == login_data.email).first()
        print("Teacher DB Query Time:", time.time() - start)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        start = time.time()
        password_ok = verify_password(login_data.password, user.password_hash)
        print("Teacher Password Verify Time:", time.time() - start)

        if not password_ok:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )

    start = time.time()

    token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email
        },
        role=login_data.role
    )

    print("Token Creation Time:", time.time() - start)
    print("Total Login Time:", time.time() - total_start)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": login_data.role,
        "user_id": user.id
    }