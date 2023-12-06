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
@router.post("/upload")
def upload_entry(
        user_id : int, 
        store_id : int,
        item_id : int,
        grocery_price : float,
        inventory_levels : inventory_levels = inventory_levels.medium       
    ):
    """ """

    if grocery_price < 0:
        return {"error" : "Price can't be less than zero"}

    with db.engine.begin() as connection:
        user_exists = connection.execute(
                sqlalchemy.text("""
                                SELECT id 
                                FROM users 
                                WHERE id = :user_id
                                """),
                [{"user_id": user_id}]).fetchone()
        
        if not user_exists:
            return {"error" : "User id does not exist."}
        
        store_exists = connection.execute(
                sqlalchemy.text("""
                                SELECT id 
                                FROM stores 
                                WHERE stores.id = :store_id
                                """),
                [{"store_id": store_id}]).fetchone()
        
        if not store_exists:
            return {"error" : "Store id does not exist."}
        
        item_exists = connection.execute(
            sqlalchemy.text("""
                                SELECT id
                                FROM items
                                WHERE items.id = :item_id
                                """),
                [{"item_id": item_id}]).fetchone()
        
        if not item_exists:
            return {"error" : "Item does not exist"}

        entry = connection.execute(
            sqlalchemy.text("""
                            WITH check_existing AS (
                                SELECT id
                                FROM crowdsourced_entries
                                WHERE item_id = :item_id and user_id = :user_id and store_id = :store_id
                            )
                            INSERT INTO crowdsourced_entries (created_at, item_id, store_id, user_id, price, inventory)
                            SELECT NOW(), :item_id, :store_id, :user_id, :grocery_price, :inventory
                            WHERE NOT EXISTS (SELECT 1 FROM check_existing)
                            RETURNING id
                            """),
            [{
                "item_id": item_id,
                "store_id": store_id,
                "user_id": user_id,
                "grocery_price": grocery_price,
                "inventory": inventory_levels
            }]).fetchone()
    
    if not entry:
        return {"error" : "Item entry already exists from user"}

    return {"posting_id":entry[0]}

@router.put("/update")
def update_entry(
        posting_id : int,
        grocery_price : float
    ):
    
    if grocery_price < 0:
        return {"error" : "Price can't be less than zero"}

    with db.engine.begin() as connection:
        entry = connection.execute(sqlalchemy.text("""
                                            UPDATE crowdsourced_entries
                                            SET price = :grocery_price
                                            WHERE id = :posting_id
                                            returning id
                                            """),[{
                                                "posting_id": posting_id,
                                                "grocery_price": grocery_price,
                                            }]).fetchone()
    
    if not entry:
        return {"error" : "Entry does not exist"}

    return {"update": "success", "entry_id" : entry[0], "price": grocery_price}
    
@router.delete("/delete")
def remove_entry(
        posting_id : int,
    ):
    with db.engine.begin() as connection:
        check = connection.execute(sqlalchemy.text(
        """
        DELETE FROM crowdsourced_entries
        WHERE id = :posting_id
        returning id
        """),[{"posting_id": posting_id}]).fetchone()
    
    if not check:
        return {"error": "posting does not exist"}
    
    return {"delete": "success"}
