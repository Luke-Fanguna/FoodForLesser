from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum


router = APIRouter(
prefix="/lists",
tags=["list"],
dependencies=[Depends(auth.get_api_key)],
)


class NewList(BaseModel):
    customer: str




@router.post("/")
def create_list(new_list: NewList):
    """ """

    return {"list_id": 1}




@router.get("/{list_id}")
def get_list(list_id: int):
    """ """


    return {}




class ListItem(BaseModel):
    quantity: int




@router.post("/{list_id}/items/{item_name}")
def set_item_quantity(list_id: int, item_name: str, list_item: ListItem):
    """ """


    return "OK"




@router.delete("/{list_id}/items/{item_name}")
def delete_item(list_id: int, item_name: str):
    """ Deletes item specified by item_name in the list that is specified by list_id """


    return "OK"


