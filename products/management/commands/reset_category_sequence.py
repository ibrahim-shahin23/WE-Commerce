from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Resets the sequence for the Category table"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval('products_category_id_seq', (SELECT MAX(id) FROM products_category));")
        self.stdout.write(self.style.SUCCESS('Successfully reset the sequence for Category'))