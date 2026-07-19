from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_verified_user
from app.models.user import User
from app.core.database import get_db

 
router = APIRouter(
    prefix="/users",
    tags=["user"],
    dependencies=[Depends(get_verified_user)]
)

@router.get("/search")
def search_users(
    email: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user),
):


    users = (
        db.query(User)
        .filter(
            User.email.ilike(f"%{email}%"),
            User.id != current_user.id,
            User.is_verified == True
        )
        .limit(10)
        .all()
    )


    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]