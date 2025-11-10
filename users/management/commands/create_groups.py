from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Создает стандартные группы пользователей (например, Модераторы)"

    def handle(self, *args, **options):
        group_names = ["Модераторы"]
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Создана группа: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Группа уже существует: {name}"))
