# utils/type_utils.py
from decimal import Decimal

def to_decimal(value):
    """Safely convert any numeric value to Decimal"""
    if isinstance(value, Decimal):
        return value
    elif isinstance(value, (int, float)):
        return Decimal(str(value))
    elif isinstance(value, str):
        try:
            return Decimal(value)
        except:
            return Decimal('0')
    else:
        return Decimal('0')

def to_float(value):
    """Safely convert any numeric value to float"""
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, str):
        try:
            return float(value)
        except:
            return 0.0
    else:
        return 0.0