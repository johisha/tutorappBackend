from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Teacher, Review
from app.schemas.schemas import TeacherProfile, NearbySearch
from fastapi import HTTPException, status
from typing import List, Optional
import math


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two points in kilometers"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad, lng1_rad = math.radians(lat1), math.radians(lng1)
    lat2_rad, lng2_rad = math.radians(lat2), math.radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    c = 2 * math.asqrt(a)
    
    return R * c


def get_all_teachers(db: Session):
    teachers = db.query(Teacher).filter(Teacher.is_verified == True).all()
    
    result = []
    for teacher in teachers:
        review_count = db.query(Review).filter(Review.teacher_id == teacher.id).count()
        avg_rating = db.query(Review.rating).filter(Review.teacher_id == teacher.id).avg()
        
        teacher_dict = {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "phone": teacher.phone,
            "profile_photo_url": teacher.profile_photo_url,
            "experience": teacher.experience,
            "subjects": teacher.subjects,
            "hourly_fee": teacher.hourly_fee,
            "address": teacher.address,
            "latitude": teacher.latitude,
            "longitude": teacher.longitude,
            "is_verified": teacher.is_verified,
            "rating": avg_rating if avg_rating else None,
            "review_count": review_count
        }
        result.append(teacher_dict)
    
    return result


def get_teacher_by_id(db: Session, teacher_id: int):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id, Teacher.is_verified == True).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    review_count = db.query(Review).filter(Review.teacher_id == teacher.id).count()
    avg_rating = db.query(Review.rating).filter(Review.teacher_id == teacher.id).avg()
    
    teacher_dict = {
        "id": teacher.id,
        "name": teacher.name,
        "email": teacher.email,
        "phone": teacher.phone,
        "profile_photo_url": teacher.profile_photo_url,
        "experience": teacher.experience,
        "subjects": teacher.subjects,
        "hourly_fee": teacher.hourly_fee,
        "address": teacher.address,
        "latitude": teacher.latitude,
        "longitude": teacher.longitude,
        "is_verified": teacher.is_verified,
        "rating": avg_rating if avg_rating else None,
        "review_count": review_count
    }
    
    return teacher_dict


def update_teacher_profile(db: Session, teacher_id: int, profile_data: TeacherProfile):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(teacher, field, value)
    
    db.commit()
    db.refresh(teacher)
    
    return teacher


def get_teachers_nearby(db: Session, lat: float, lng: float, radius: float = 5):
    teachers = db.query(Teacher).filter(Teacher.is_verified == True).all()
    
    result = []
    for teacher in teachers:
        if teacher.latitude and teacher.longitude:
            distance = haversine_distance(lat, lng, teacher.latitude, teacher.longitude)
            
            if distance <= radius:
                review_count = db.query(Review).filter(Review.teacher_id == teacher.id).count()
                avg_rating = db.query(Review.rating).filter(Review.teacher_id == teacher.id).avg()
                
                teacher_dict = {
                    "id": teacher.id,
                    "name": teacher.name,
                    "email": teacher.email,
                    "phone": teacher.phone,
                    "profile_photo_url": teacher.profile_photo_url,
                    "experience": teacher.experience,
                    "subjects": teacher.subjects,
                    "hourly_fee": teacher.hourly_fee,
                    "address": teacher.address,
                    "latitude": teacher.latitude,
                    "longitude": teacher.longitude,
                    "is_verified": teacher.is_verified,
                    "rating": avg_rating if avg_rating else None,
                    "distance": distance,
                    "review_count": review_count
                }
                result.append(teacher_dict)
    
    # Sort by distance
    result.sort(key=lambda x: x["distance"])
    
    return result