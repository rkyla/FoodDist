from fastapi import APIRouter
from app.services.restaurant_service import RestaurantService

router = APIRouter()
restaurant_service = RestaurantService()

@router.get("/search/{restaurant_name}")
async def search_restaurant(restaurant_name: str):
    return await restaurant_service.search_restaurant(restaurant_name)

@router.get("/menu/{restaurant_name}")
async def get_menu(restaurant_name: str):
    return await restaurant_service.get_menu(restaurant_name)