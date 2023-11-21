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
        WHERE username LIKE :username OR email LIKE :email;
        ''')
        ,[{'username':username, 'email':email}]).scalar()

        if entry:
            return 'Username or Email already in use'
       
       # if it does not exist, add to db
        id = connection.execute(sqlalchemy.text(
        '''
        INSERT INTO users
        (username, email)
        VALUES
        (:username,:email)
        RETURNING id
        '''    
        )
        ,[{'username':username,'email':email}]).scalar()
        
        return { 'user_id' : id }