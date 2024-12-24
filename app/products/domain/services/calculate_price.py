def calculate_price(cost: float, margin: float) -> float:

    if cost < 0 or margin < 0 or margin >= 100:
        raise ValueError("Cost must be non-negative and margin must be between 0 and 100.")

    price = cost / (1 - margin / 100)
    return round(price, 2)