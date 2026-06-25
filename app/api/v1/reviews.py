from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import ReviewCreate, ReviewResponse
from app.models.models import Review, Student, Teacher
from app.utils.auth import decode_token

router = APIRouter(prefix="/reviews", tags=["Reviews"])


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
def create_review(
    review_data: ReviewCreate,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Create a review for a teacher"""
    teacher = db.query(Teacher).filter(Teacher.id == review_data.teacher_id).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    review = Review(
        student_id=current_student.id,
        teacher_id=review_data.teacher_id,
        rating=review_data.rating,
        review=review_data.review
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    return {"message": "Review created successfully"}


@router.get("/{teacher_id}")
def get_teacher_reviews(teacher_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a teacher"""
    reviews = db.query(Review).filter(Review.teacher_id == teacher_id).all()
    
    result = []
    for review in reviews:
        student = db.query(Student).filter(Student.id == review.student_id).first()
        result.append({
            "id": review.id,
            "student_id": review.student_id,
            "teacher_id": review.teacher_id,
            "rating": review.rating,
            "review": review.review,
            "created_at": review.created_at,
            "student_name": student.name if student else "Unknown"
        })
    
    return result