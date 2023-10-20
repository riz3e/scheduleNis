from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import classf



router = APIRouter()


@router.get('/{id}', tags=['time table'])
async def get_tt(id: int = None):
    return classf.final(id)


