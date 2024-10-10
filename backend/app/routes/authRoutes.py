from fastapi import HTTPException, status, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from ..models import userModel
from ..db import database
from ..schemas import tokenSchema
from ..authentication import oauth2
from ..utils import utils
from ..utils.limiter import limiter

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=tokenSchema.TokenResponse
)
@limiter.limit("3/hour")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(userModel.User)
        .filter(userModel.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
