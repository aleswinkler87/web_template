from django.core.management.base import BaseCommand
from myapp.models import Item

class Command(BaseCommand):
    help = "Populate the database with sample items"

    def handle(self, *args, **kwargs):
        items = [
            {"name": "Sword of Destiny", "description": "A legendary sword with magical powers."},
            {"name": "Healing Potion", "description": "A potion that restores health."},
            {"name": "Shield of Valor", "description": "A strong shield used by ancient warriors."},
            {"name": "Magic Scroll", "description": "A scroll containing a powerful spell."},
            {"name": "Mystic Amulet", "description": "An enchanted amulet that grants wisdom."},
        ]

        for item_data in items:
            item, created = Item.objects.get_or_create(name=item_data["name"], defaults=item_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created item: {item.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Item already exists: {item.name}"))

        self.stdout.write(self.style.SUCCESS("Database successfully populated with items."))