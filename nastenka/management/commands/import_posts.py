import json
from pathlib import Path
from django.core.management.base import BaseCommand
from nastenka.models import Post


class Command(BaseCommand):
    help = 'Importuje příspěvky z posts.json do databáze'

    def handle(self, *args, **options):
        json_path = Path(__file__).resolve().parents[3] / 'posts.json'
        if not json_path.exists():
            self.stderr.write(f'Soubor nenalezen: {json_path}')
            return

        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        created = 0
        for item in data:
            attachment = item.get('attachment') or {}
            _, was_created = Post.objects.get_or_create(
                title=item['title'],
                defaults={
                    'description': item.get('description', ''),
                    'type': item.get('type', 'info'),
                    'icon': item.get('icon', 'info'),
                    'date': item.get('date', ''),
                    'time': item.get('time') or '',
                    'location': item.get('location') or '',
                    'attachment_name': attachment.get('name', ''),
                    'attachment_size': attachment.get('size', ''),
                }
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Importováno {created} příspěvků (z {len(data)} celkem).'))
