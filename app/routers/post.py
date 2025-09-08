from .. import models, schemas, oauth2
from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import Sessionlocal, get_db
from typing import List ,Optional
from  ..schemas import PostOut

router = APIRouter(
    prefix="/posts",
    tags= ["Posts"]
  
)






@router.get("/",response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10 , skip :int = 0, search: Optional[str] = " "):
    
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post,func.count(models.Votes.post_id) .label("votes")).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
    return results



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.responsePost)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user) ):
   

    
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post       

@router.get("/{id}",response_model=PostOut)
def get_post(id: int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):


   
  # post = db.query(models.Post).filter(models.Post.id == id).first()
   post = db.query(models.Post,func.count(models.Votes.post_id) .label("votes")).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
   if not post: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found") 

   return post    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

   

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")  
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized access")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
   
    
    db_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = db_post.first()  
    if updated_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized access")
    db_post.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)

    return  updated_post