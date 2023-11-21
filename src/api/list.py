from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
prefix="/lists",
tags=["list"],
dependencies=[Depends(auth.get_api_key)],
)

@router.post("/")
def create_list(user_id: int):
    """ """
    with db.engine.begin() as connection:
        result = connection.execute(
                sqlalchemy.text("""
                                INSERT INTO grocery_list (user_id)
                                SELECT :user_id
                                RETURNING id
                                """),
                [{
                    "user_id": user_id,
                }]).scalar_one()
    
    return {"list_id": result}

@router.get("/{list_id}")
def get_list(list_id : int):
    """ """
    with db.engine.begin() as connection:
        items = connection.execute(
                sqlalchemy.text("""
                                SELECT item_id, items.Name, quantity
                                FROM grocery_list_items
                                JOIN items on items.id = grocery_list_items.item_id
                                WHERE grocery_list_items.list_id = :list_id
                                """),
                [{
                    "list_id": list_id,
                }]).fetchall()

    res = []

    for item in items:
        res.append({"item_id": item[0], 
                    "item": item[1], 
                    "quantity": item[2]})
    return res


class ListItem(BaseModel):
    quantity: int


@router.post("/{list_id}/items/{item_id}/{quantity}")
def set_item_quantity(list_id: int, item_id: int, quantity: int):
    """ """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("""
                            INSERT INTO grocery_list_items (list_id, item_id, quantity)
                            SELECT :list_id, :item_id, :quantity
                            RETURNING id
                            """),
            [{
                "list_id": list_id,
                "item_id": item_id,
                "quantity": quantity,
            }]).scalar_one()
    
    return {"posting_id": result}

@router.put("/{posting_id}/items/{quantity}")
def update_posting(posting_id: int, quantity : int):
    """ """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                            UPDATE grocery_list_items
                            SET quantity = :quantity
                            WHERE id = :posting_id
                            """),
            [{
                "quantity": quantity,
                "posting_id": posting_id,
            }])    
    return "OK"


@router.delete("/{posting_id}/items/")
def delete_item(posting_id: int):
    """ Deletes item specified by item_name in the list that is specified by list_id """

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                            DELETE FROM grocery_list_items
                            WHERE id = :posting_id
                            """),
            [{
                "posting_id": posting_id,
            }])

    return "OK"