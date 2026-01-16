from fastapi import FastAPI
from api.users import router as user_router
from api.auth import router as auth_router
from api.restaurants import router as restaurant_router
from api.menu import router as menu_router
from api.cart import router as cart_router
from api.orders import router as order_router
from api.payments import router as payment_router
from api.delivery import router as delivery_router
from api.admin_orders import router as admin_orders_router
from api.admin_restaurants import router as admin_restaurants_router
from api.admin_delivery import router as admin_delivery_router
from api.admin_payouts import router as admin_payouts_router
from api.tracking import router as tracking_router

app = FastAPI(title="Swiggy_backend")
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(menu_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(delivery_router)
app.include_router(admin_orders_router)
app.include_router(admin_restaurants_router)
app.include_router(admin_delivery_router)
app.include_router(admin_payouts_router)
app.include_router(tracking_router)

@app.get("/")
def health():
    return {"status": "Swiggy backend Running"}

