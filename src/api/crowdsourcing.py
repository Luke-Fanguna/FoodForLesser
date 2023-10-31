from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/crowdsourcing",
    tags=["crowdsourcing"],
    dependencies=[Depends(auth.get_api_key)],
)

class inventory_levels(str, Enum):
    high = "high"
    medium = "medium"  
    low = "low"

# posts a crowdsource listing
@router.post("/{user_id}/upload/{store_id}/{item_id}/{grocery_price}")
def upload_entry(
        user_id : int, 
        store_id : int,
        item_id : int,
        grocery_price : float,
        inventory_levels : inventory_levels = inventory_levels.medium       
    ):
    """ """

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("""
                            INSERT INTO crowdsourced_entries (created_at, item_id, store_id, user_id, price, inventory)
                            SELECT NOW(), :item_id, :store_id, :user_id, :grocery_price, :inventory
                            RETURNING id
                            """),
            [{
                "item_id": item_id,
                "store_id": store_id,
                "user_id": user_id,
                "grocery_price": grocery_price,
                "inventory": inventory_levels
            }]).scalar_one()
    
    return result

@router.put("/{posting_id}/update/{grocery_price}")
def get_bottle_plan(
        posting_id : int,
        grocery_price : float
    ):
    
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                            UPDATE crowdsourced_entries
                                            SET price = :grocery_price
                                            WHERE id = :posting_id
                                            """),[{
                                                "posting_id": posting_id,
                                                "grocery_price": grocery_price,
                                            }])
        
    return "OK"
    
@router.delete("/{posting_id}/delete")
def remove_entry(
        posting_id : int,
    ):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
        """
        DELETE FROM crowdsourced_entries
        WHERE id = :posting_id
        """),[{"posting_id": posting_id}])
        
    return "OK"
