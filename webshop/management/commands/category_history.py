from django.core.management.base import BaseCommand
from webshop.models import Category


class Command(BaseCommand):
    help = 'Displays the history of a category'

    def add_arguments(self, parser):
        parser.add_argument('category_identifier', help='Category ID or Category Slug')

    def handle(self, *args, **options):
        category_identifier = options['category_identifier']
        try:
            if category_identifier.isdigit():
                category = Category.objects.get(pk=category_identifier)
            else:
                category = Category.objects.get(category_slug=category_identifier)
            
            history = category.history.all()
            self.stdout.write(f"History for category {category.category_name} (ID: {category.id}, Slug: {category.category_slug}):")
            for historical_category in history:
                self.stdout.write(f"Version: {historical_category.history_id}")
                for field in historical_category._meta.fields:
                    field_name = field.name
                    field_value = getattr(historical_category, field_name)
                    self.stdout.write(f"{field_name}: {field_value}")
                self.stdout.write('')
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Category with ID or Slug '{category_identifier}' does not exist."))