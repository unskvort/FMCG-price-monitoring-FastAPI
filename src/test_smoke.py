import syspath

syspath.append_current_path()
syspath.append_git_root()
syspath.append_parent_path()
from fastapi.testclient import TestClient

from dependencies import app
from routers import categories, prices, products, users

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(prices.router)
app.include_router(users.router)

client = TestClient(app)


def test_categories() -> None:
    response = client.get("/categories")
    assert response.status_code == 401


def test_products() -> None:
    response = client.get("/products")
    assert response.status_code == 401


def test_prices() -> None:
    response = client.get("/prices")
    assert response.status_code == 401
