from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
prefix="/lists",
tags=["list"],
dependencies=[Depends(auth.get_api_key)],
)

@router.post("/stores/{list_id}/distribute (POST)")
def distribute_list(list_id: int):
    """ """


@router.post("/stores/{list_id}/best (POST)")
def find_best_item(list_id: int):
    """ """

@router.post("/stores/ (GET)")
def find_stores():
    """ """
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT id, name 
            FROM stores
            ORDER BY id ASC
            """
            )).fetchall()
    
    stores = []
    for store in result:
        stores.append(
            {
                "id": store[0],
                "name": store[1]
            }
        )
    return stores