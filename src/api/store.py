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

# gets the list_id and then checks which stores have the best price
# list_id 
# get item_id with list_id from grocery_list_items
# with item_id, find the smallest for each value and unique values are found with list_id
# list_id == user_id
@router.post("/stores/{list_id}/distribute (POST)")
def distribute_list(list_id: int):
    """ """
    with db.engine.begin() as connection:
        # gets every item from list_id
        items = connection.execute(sqlalchemy.text(
        """
        SELECT
            item_id
        WHERE list_id = :list_id
        """
        ),[{"list_id":list_id}]).fetchall()
        if items[0] == None:
            return []
        items = list(items)
        best = []
        
        # searches crowdsources entries for best price
        for item in items:
            best = connection.execute(sqlalchemy.text(
            """
            SELECT 
                store_id,
                MIN(price)
            FROM crowdsourced_entries
            WHERE item_id = :item_id
            ORDER BY store_id asc;
            """
            ),[{"item_id":item}]).fetchall()
            
            distribute = []
            # joins best prices items with their stores
            distribute.append([connection.execute(sqlalchemy.text(
            """
            SELECT
                name
            FROM stores
            WHERE store_id = :store_id
            """
            ),[{"store_id":best[0]}]).fetchone()[0],best[1]])
        
        return distribute
        


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