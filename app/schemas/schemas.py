from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Authentication
class StudentRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    phone: str
    password: str = Field(..., min_length=6)
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TeacherRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    phone: str
    password: str = Field(..., min_length=6)
    aadhaar_url: Optional[str] = None
    voter_id_url: Optional[str] = None
    qualification_url: Optional[str] = None
    experience:  Optional[int] = None
    subjects: str
    hourly_fee: Optional[float] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Login(BaseModel):
    email: str
    password: str
    role: str = Field(..., pattern="^(student|teacher|admin)$")


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


# Student
class StudentProfile(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# Teacher
class TeacherProfile(BaseModel):
    name: Optional[str] = None
    profile_photo_url: Optional[str] = None
    experience: Optional[int] = None
    subjects: Optional[str] = None
    hourly_fee: Optional[float] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TeacherResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    profile_photo_url: Optional[str]
    experience: int
    subjects: str
    hourly_fee: float
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    is_verified: bool
    rating: Optional[float] = None
    distance: Optional[float] = None
    
    class Config:
        from_attributes = True


# Review
class ReviewCreate(BaseModel):
    teacher_id: int
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    rating: int
    review: Optional[str]
    created_at: datetime
    student_name: str
    
    class Config:
        from_attributes = True


# Demo Request
class DemoRequestCreate(BaseModel):
    teacher_id: int


class DemoRequestResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    status: str
    created_at: datetime
    student_name: str
    teacher_name: str
    
    class Config:
        from_attributes = True


# Admin
class PendingTeacherResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    experience: int
    subjects: str
    hourly_fee: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# Location Search
class NearbySearch(BaseModel):
    lat: float
    lng: float
    radius: float = Field(default=5, gt=0)