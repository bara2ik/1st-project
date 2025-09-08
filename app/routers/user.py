from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, Sessionlocal, get_db



router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)


@router.get("/list",response_model=list[schemas.responseUser]) 
def get_allusers(db: Session = Depends(get_db)):
    #ursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()  
    users = db.query(models.User).all()
    return users

@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.responseUser)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    pwsd_hash = utils.hash(user.password)
    user.password = pwsd_hash
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.responseUser)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} was not found")      
    return user
