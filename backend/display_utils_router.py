from fastapi import APIRouter

from display_utils import display_utils

router = APIRouter()


@router.get("/clear")
async def display_utils_root():
    try:
        print("Tried cleaning display")
        display_utils.clear_display()
        return {"message": "Display cleared."}
    except Exception as e:
        raise Exception(e)
