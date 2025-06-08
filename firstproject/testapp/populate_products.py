import os
import sys
import django
import random 
import requests

# Add the parent directory to the Python path so Django can find the firstproject module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstproject.settings')
django.setup()

from testapp.models import Product

response = requests.get("https://dummyjson.com/products?limit=100")
data = response.json()['products']

for item in data:
    Product.objects.create(
        name= item['title'],
        category=item['category'],
        price=item['price'],
        description=item['description'],
        stock=item['stock'],
        rating=item['rating'],
        image_url=item['thumbnail']
    )


print("100 mock products added")