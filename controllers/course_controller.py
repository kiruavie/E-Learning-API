from sqlmodel import Session, select
from models.course import Course
from models.user import User
from schemas.course_schema import CourseCreate, CourseUpdate
from typing import List, Optional


def create_course(db: Session, course: CourseCreate, instructor_id: int):
    """Créer un nouveau cours avec l'ID de l'instructeur authentifié"""
    # L'utilisateur est déjà vérifié comme instructeur par la dépendance
    
    new_course = Course(
        title=course.title,
        description=course.description,
        instructor_id=instructor_id  # Utilise l'ID de l'utilisateur connecté
    )
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


def get_course(db: Session, course_id: int):
    """Récupérer un cours par ID"""
    statement = select(Course).where(Course.id == course_id)
    course = db.exec(statement).first()
    
    if not course:
        raise ValueError("Cours introuvable")
    
    return course


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    """Récupérer tous les cours avec pagination"""
    statement = select(Course).offset(skip).limit(limit)
    courses = db.exec(statement).all()
    return courses


def get_courses_by_instructor(db: Session, instructor_id: int):
    """Récupérer tous les cours d'un instructeur"""
    statement = select(Course).where(Course.instructor_id == instructor_id)
    courses = db.exec(statement).all()
    return courses


def update_course(db: Session, course_id: int, course_update: CourseUpdate):
    """Mettre à jour un cours"""
    statement = select(Course).where(Course.id == course_id)
    course = db.exec(statement).first()
    
    if not course:
        raise ValueError("Cours introuvable")
    
    # Mettre à jour seulement les champs fournis
    update_data = course_update.dict(exclude_unset=True)
    
    # Si instructor_id est modifié, vérifier qu'il est valide
    if "instructor_id" in update_data:
        statement = select(User).where(User.id == update_data["instructor_id"])
        instructor = db.exec(statement).first()
        
        if not instructor:
            raise ValueError("Instructeur introuvable")
        
        if instructor.role != "instructor":
            raise ValueError("L'utilisateur doit avoir le rôle 'instructor'")
    
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: int):
    """Supprimer un cours"""
    statement = select(Course).where(Course.id == course_id)
    course = db.exec(statement).first()
    
    if not course:
        raise ValueError("Cours introuvable")
    
    db.delete(course)
    db.commit()
    return {"message": "Cours supprimé avec succès"}


def get_course_with_instructor(db: Session, course_id: int):
    """Récupérer un cours avec les informations de l'instructeur"""
    statement = select(Course, User).join(User).where(Course.id == course_id)
    result = db.exec(statement).first()
    
    if not result:
        raise ValueError("Cours introuvable")
    
    course, instructor = result
    
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "instructor_id": course.instructor_id,
        "instructor_name": instructor.name,
        "instructor_email": instructor.email
    }