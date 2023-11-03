from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
prefix="/lists",
tags=["list"],
dependencies=[Depends(auth.get_api_key)],
)

