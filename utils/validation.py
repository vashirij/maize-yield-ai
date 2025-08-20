def validate_range(value, min_val, max_val):
    try:
        v = float(value)
        return min_val <= v <= max_val
    except ValueError:
        return False
