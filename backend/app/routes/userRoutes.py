from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from ..models import userModel
from ..db.database import get_db
from ..schemas import userSchema
from ..utils import utils
from ..utils.limiter import limiter


router = APIRouter(prefix="/users", tags=["User"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=userSchema.UserResponse,
)
@limiter.limit("3/minute")
def register_user(user: userSchema.CreateUser, db: Session = Depends(get_db)):
    existing_username = (
        db.query(userModel.User)
        .filter(userModel.User.username == user.username)
        .first()
    )

    existing_email = (
        db.query(userModel.User).filter(userModel.User.email == user.email).first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This Username Is Already Taken.",
        )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This E-mail Is Already Taken."
        )

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = userModel.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
