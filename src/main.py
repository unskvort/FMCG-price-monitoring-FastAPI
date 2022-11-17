from dependencies import app, db
from internal.tasks import scheduler
from routers import categories, prices, products, users


@app.on_event("startup")
def on_startup() -> None:
    db.init_db()
    scheduler.start()


@app.get("/")
def healthcheck() -> dict:  # type: ignore
    return {"ping": "pong!"}


app.include_router(categories.router)
app.include_router(products.router)
app.include_router(prices.router)
app.include_router(users.router)
