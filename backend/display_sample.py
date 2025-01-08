from display_main import display_text_at_position
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def display_utils_root():
    try:
        modules = [
            {"type": "email", "start_position": 5},
            {"type": "weather", "start_position": 4},
            {"type": "traffic", "start_position": 1},
        ]

        display_text_at_position(modules)

        return {"message": "Display successfully rendered sample."}
    except:
        return {"message": "Failed to render sample."}
