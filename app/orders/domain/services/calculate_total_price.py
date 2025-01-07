from app.products.domain.entities.product import Product
def calculate_total_price(products: list[Product]) -> float:
    total_price = sum(product.price.get() for product in products)
    return round(total_price, 2)