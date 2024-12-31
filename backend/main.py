from apscheduler.schedulers.background import BackgroundScheduler
from display_sample import router as display_sample_router
from display_utils_router import router as display_utils_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from render_display_router.render_display_router import \
    router as render_display_router
from tortoise.contrib.fastapi import register_tortoise
from weather import router as weather_router

app = FastAPI()
scheduler = BackgroundScheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def test_task():
    print("Every 30 seconds.")


scheduler.add_job(test_task, "interval", seconds=10)
scheduler.start()


register_tortoise(
    app,
    db_url="sqlite://test.db",
    modules={"models": [
        "database.module_settings.weather",
        "database.module_settings.email",
        "database.module_settings.stocks",
        "database.module_settings.traffic",
        "database.module_settings.news",
        "database.display_settings.display",
    ]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/")
async def root():
    return {"message": "Beep Beep!"}


# Include the weather router
app.include_router(weather_router, prefix="/weather")
app.include_router(display_utils_router, prefix="/display-utils")
app.include_router(display_sample_router, prefix="/display-sample")
app.include_router(render_display_router, prefix="/render")


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
