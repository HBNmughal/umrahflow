from django.http import HttpResponse
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

def generate_barcode(request, barcode_data):
    # Data for the barcode
    barcode_data = barcode_data
    
    # Create barcode
    barcode = Code128(barcode_data, writer=ImageWriter())
    
    # Save barcode to a BytesIO object
    buffer = BytesIO()
    barcode.write(buffer)
    buffer.seek(0)
    
    # Convert BytesIO to Image
    image = Image.open(buffer)
    
    # Save to HttpResponse
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response