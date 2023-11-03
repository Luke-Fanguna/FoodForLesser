from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
prefix="/lists",
tags=["list"],
dependencies=[Depends(auth.get_api_key)],
)

@router.post("/stores/{list_id}/distribute (POST)")
def distribute_list():
    """ """


@router.post("/stores/{list_id}/best (POST)")
def find_best_item():
    """ """

@router.post("/stores/ (GET)")
def find_stores():
    """ """
