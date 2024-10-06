from fastapi import APIRouter, HTTPException
from app.services.restaurant_service import RestaurantService

router = APIRouter()
restaurant_service = RestaurantService()

@router.get("/search/{restaurant_name}")
async def search_restaurant(restaurant_name: str):
    return await restaurant_service.search_restaurant(restaurant_name)

@router.get("/menu/{restaurant_name}")
async def get_menu(restaurant_name: str):
    return await restaurant_service.get_menu(restaurant_name)

@router.get("/compute_similarities")
async def compute_similarities():
    result = restaurant_service.compute_similarities()
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result