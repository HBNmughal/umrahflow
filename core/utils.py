from django.utils import timezone
from umrahflow.settings import VAT_PERCENTAGE
from decimal import Decimal

def calculate_tax(price_including_vat, vat_rate=VAT_PERCENTAGE):
    # Convert vat_rate to float
    vat_rate = Decimal(vat_rate)
    # Calculate the tax multiplier
    tax_multiplier = vat_rate / Decimal(100.00)
    # Calculate the tax amount
    tax_amount = Decimal(price_including_vat) - Decimal(price_including_vat / (1 + tax_multiplier))
    return Decimal(tax_amount)