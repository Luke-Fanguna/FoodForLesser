from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum


router = APIRouter(
prefix="/stores",
tags=["store"],
dependencies=[Depends(auth.get_api_key)],
)




