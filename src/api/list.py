import sqlalchemy
import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db

router = APIRouter(
prefix="/lists",
tags=["list"],
dependencies=[Depends(auth.get_api_key)],
)

@router.post("/create")
def create_list(user_id: int, list_name: str):
    """
    * Complex endpoint *

    Creates a new grocery list with the name passed in
    for the user correlated to user_id.

    Returns an error if the list_name already exists
    under the same user or if the user does not exist
    """

    with db.engine.begin() as connection:
        dup_list = connection.execute(
                sqlalchemy.text("""
                                SELECT list_name
                                FROM grocery_list 
                                WHERE user_id = :user_id and list_name = :list_name
                                """),
                [{"user_id": user_id, "list_name": list_name}]).fetchone()
        
        if dup_list:
            return {"error" : "List with name already exists. Please choose a different name."}
        
        user_exists = connection.execute(
                sqlalchemy.text("""
                                SELECT id 
                                FROM users 
                                WHERE id = :user_id
                                """),
                [{"user_id": user_id}]).fetchone()
        
        if not user_exists:
            return {"error" : "User id does not exist."}

        list_id = connection.execute(
                sqlalchemy.text("""
                                INSERT INTO grocery_list (list_name, user_id)
                                VALUES (:list_name, (:user_id))
                                RETURNING id
                                """),
                [{"user_id": user_id, "list_name": list_name}]).scalar_one()
    
    return {"list_id": list_id}


@router.get("/get/{list_id}")
def get_list(list_id : int):
    """ """
    with db.engine.begin() as connection:
        list_exists = connection.execute(
            sqlalchemy.text("""
                                SELECT id
                                FROM grocery_list
                                WHERE grocery_list.id = :list_id
                                """),
                [{"list_id": list_id}]).fetchone()
        
        if not list_exists:
            return {"error" : "List id does not exist."}

        items = connection.execute(
                sqlalchemy.text("""
                                SELECT gli.id, item_id, items.item_name, quantity
                                FROM grocery_list_items as gli
                                JOIN items on items.id = gli.item_id
                                WHERE gli.list_id = :list_id
                                """),
                [{"list_id": list_id}]).fetchall()

    res_list = []

    for item in items:
        res_list.append({"posting_id": item[0],
                         "item_id": item[1], 
                    "item": item[2], 
                    "quantity": item[3]})
    return res_list


@router.get("/get")
def get_items():
    with db.engine.begin() as connection:
        items = connection.execute(
            sqlalchemy.text("""
                            SELECT DISTINCT id, item_name FROM items
                            """)).fetchall()
        
    items = [(int(item[0]),str(item[1])) for item in items]
    item_list = {key: value for key, value in items}

    return item_list

class ListItem(BaseModel):
    quantity: int


@router.post("/create/item_quantity")
def set_item_quantity(list_id: int, item_id: int, quantity: int):
    """
    Adds a new item to the grocery list with the given list name
    """

    if quantity < 1:
        return {"error": "quantity must be greater than 0"}

    with db.engine.begin() as connection:
        posting_id = connection.execute(
            sqlalchemy.text("""
                            WITH check_existing AS (
                                SELECT id
                                FROM grocery_list_items
                                WHERE list_id = :list_id and item_id = :item_id
                            )
                            INSERT INTO grocery_list_items (list_id, item_id, quantity)
                            SELECT :list_id, :item_id, :quantity
                            WHERE NOT EXISTS (SELECT 1 FROM check_existing)
                            RETURNING id
                            """),
            [{
                "list_id": list_id,
                "item_id": item_id,
                "quantity": quantity,
            }]).fetchone()
    
    if not posting_id:
        return {"error" : "Item already entered into list"}

    return {"posting_id": posting_id[0]}


@router.put("/{posting_id}/items/{quantity}")
def update_list(posting_id: int, quantity : int):
    """ 
    Updates the quantity of the item in grocery list 
    specified by the posting_id passed in 
    """

    if quantity < 1:
        return {"error": "quantity must be greater than 0"}

    with db.engine.begin() as connection:
        check = connection.execute(
            sqlalchemy.text("""
                            UPDATE grocery_list_items
                            SET quantity = :quantity
                            WHERE id = :posting_id
                            returning id
                            """),
            [{
                "quantity": quantity,
                "posting_id": posting_id,
            }]).fetchone()
    
    if not check:
        return {"error": "posting does not exist"}
        
    return {"update": "success", "posting_id": check[0], "quantity" : quantity }


@router.delete("/{posting_id}/items/")
def delete_item(posting_id: int):
    """ 
    Deletes item specified by posting_id in the list 
    """

    with db.engine.begin() as connection:
        check = connection.execute(
            sqlalchemy.text("""
                            DELETE FROM grocery_list_items
                            WHERE id = :posting_id
                            returning id
                            """),
            [{
                "posting_id": posting_id,
            }]).fetchone()

    if not check:
        return {"error": "posting does not exist"}
    
    return {"delete": "success"}