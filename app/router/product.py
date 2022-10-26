from fastapi import APIRouter, Path
from db.productJson import product_list

router = APIRouter(
    prefix='/products',
    tags=['products']
        )

@router.get('/')
def get_all_products():
    return product_list

@router.get('/id/{product_id}')
def get_product_by_id(product_id: str = Path(None, description="Test")):
    return next(
        (product for product in product_list if product['id'] == product_id), 
        None
            )

@router.get("/{category}")
def get_product_by_category(category):
    category_list = []
    for product in product_list:
        if product['category'].upper() == category.upper():
            category_list.append(product)
    return category_list
