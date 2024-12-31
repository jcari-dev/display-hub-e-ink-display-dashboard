from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def weather_root():
    return {"message": "Base Weather URL."}
