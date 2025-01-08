from display_main import display_text_at_position
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/")
async def render_display(request: Request):
    try:
        body = await request.body()
        print("Raw body:", body.decode("utf-8"))

        json_body = await request.json()
        modules = json_body["modules"]

        print("display_text_at_position type:", type(display_text_at_position))
        print("Let's draw the screen")

        await display_text_at_position(modules)  # Proper await
    except Exception as e:
        print("Error in render_display:", str(e))
