from jose import JWTError, jwt
from datetime import datetime , timedelta
from . import schemas , database, models
from fastapi import status,Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from .config import settings 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



secret_key = settings.secret_key
algorithm = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt  


def verify_access_token(token: str, credentials_exception):

    try : 
        payload = jwt.decode(token, secret_key,algorithms=[algorithm])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.tokendata(id=id)
    except JWTError : 
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db :session = Depends(database.get_db)  ):

    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"couldnt validate credentials", headers={"WWW-Authenticate": "bearer"})
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

  


