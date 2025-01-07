def validate_existence(quantity: int, inventory_quantity: int) -> bool:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    elif quantity > inventory_quantity:
        raise ValueError("Quantity must be less than or equal to the available quantity. Available quantity: " + str(inventory_quantity))
    else:
        return True