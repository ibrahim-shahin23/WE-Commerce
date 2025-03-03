import os
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from products.models import Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Migrate product thumbnails from URLs to ImageField'

    def handle(self, *args, **kwargs):
        # Fetch products where the thumbnail is not empty
        products = Product.objects.exclude(thumbnail__isnull=True).exclude(thumbnail__exact='')

        for product in products:
            # Get the URL from the thumbnail field (assuming it was previously a UrlField)
            image_url = str(product.thumbnail)  # Convert ImageFieldFile to string (URL)

            if image_url and image_url.startswith(('http://', 'https://')):
                try:
                    # Download the image
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()

                    # Extract the image file name from the URL
                    image_name = os.path.basename(image_url)

                    # Define the path where the image will be saved
                    image_path = os.path.join(settings.MEDIA_ROOT, 'products', image_name)

                    # Save the image to the media directory
                    with open(image_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Update the product's thumbnail field
                    with open(image_path, 'rb') as f:
                        product.thumbnail.save(image_name, File(f), save=True)

                    self.stdout.write(self.style.SUCCESS(f'Successfully migrated thumbnail for product: {product.title}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to migrate thumbnail for product {product.title}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipping product {product.title} (invalid or missing thumbnail URL)'))