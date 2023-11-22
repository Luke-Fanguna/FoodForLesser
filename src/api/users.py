import sqlalchemy
import re
from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)
# email = [A-Za-z]+@email\.com
@router.post("/add")
def create_user(username : str, email : str):
    if not username and not email:
        return 'EMPTY USERNAME/EMAIL'
    calpoly = re.compile('[A-Za-z]+@calpoly\.edu')
    gmail = re.compile('[A-Za-z]+@gmail\.com')

    if calpoly.match(email) is None and gmail.match(email) is None:
        return 'MUST USE CALPOLY OR GMAIL EMAIL ADDRESS'
    
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