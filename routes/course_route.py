from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from schemas.course_schema import CourseCreate, CourseUpdate, CourseResponse, CourseWithInstructor
from db import get_session
from controllers import course_controller
from utils.dependencies import get_current_instructor
from models.user import User

router = APIRouter()


@router.post("/", response_model=CourseResponse)
async def create_course(
    course: CourseCreate, 
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_instructor)
):
    """Créer un nouveau cours (authentification et rôle instructor requis)"""
    try:
        return course_controller.create_course(db, course, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=100, description="Nombre maximum d'éléments à retourner"),
    db: Session = Depends(get_session)
):
    """Récupérer tous les cours avec pagination"""
    return course_controller.get_courses(db, skip=skip, limit=limit)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_session)):
    """Récupérer un cours par ID"""
    try:
        return course_controller.get_course(db, course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{course_id}/with-instructor", response_model=CourseWithInstructor)
async def get_course_with_instructor(course_id: int, db: Session = Depends(get_session)):
    """Récupérer un cours avec les informations de l'instructeur"""
    try:
        return course_controller.get_course_with_instructor(db, course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/instructor/{instructor_id}", response_model=List[CourseResponse])
async def get_courses_by_instructor(instructor_id: int, db: Session = Depends(get_session)):
    """Récupérer tous les cours d'un instructeur"""
    return course_controller.get_courses_by_instructor(db, instructor_id)


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(course_id: int, course_update: CourseUpdate, db: Session = Depends(get_session)):
    """Mettre à jour un cours"""
    try:
        return course_controller.update_course(db, course_id, course_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_session)):
    """Supprimer un cours"""
    try:
        return course_controller.delete_course(db, course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))