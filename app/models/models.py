from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    reviews = relationship("Review", back_populates="student")
    demo_requests = relationship("DemoRequest", back_populates="student")
    favorites = relationship("FavoriteTutor", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    profile_photo_url = Column(String(500))
    aadhaar_url = Column(String(500), nullable=False)
    voter_id_url = Column(String(500), nullable=False)
    qualification_url = Column(String(500), nullable=False)
    experience = Column(Integer, default=0)
    subjects = Column(String(500))
    hourly_fee = Column(Float, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(500))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    reviews = relationship("Review", back_populates="teacher")
    demo_requests = relationship("DemoRequest", back_populates="teacher")


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="reviews")
    teacher = relationship("Teacher", back_populates="reviews")


class DemoRequest(Base):
    __tablename__ = "demo_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="demo_requests")
    teacher = relationship("Teacher", back_populates="demo_requests")


class FavoriteTutor(Base):
    __tablename__ = "favorite_tutors"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="favorites")
    teacher = relationship("Teacher")