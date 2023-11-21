from fastapi import APIRouter, Depends
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/add")
def create_user(username : str, email : str):
    if not username and not email:
        return 'EMPTY USERNAME/EMAIL'
    
    with db.engine.begin() as connection:
        # check if the user already exists
        entry = connection.execute(sqlalchemy.text(
        '''
        SELECT
        *
        FROM users
        WHERE name LIKE :name OR email LIKE :mail;
        ''')
        ,[{'name':username, 'mail':email}]).scalar()
        print(entry)
        if entry:
            return 'Username or Email already in use'
       
       # if it does not exist, add to db
        id = connection.execute(sqlalchemy.text(
        '''
        INSERT INTO users
        (name, email)
        VALUES
        (:name,:email)
        RETURNING id
        '''    
        )
        ,[{'name':username,'email':email}]).scalar()
        
        return { 'user_id' : id }
        