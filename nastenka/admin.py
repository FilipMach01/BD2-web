from django.contrib import admin
from django.utils.html import format_html

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'icon_preview', 'date', 'created_at')
    list_filter = ('type',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    fieldsets = (
        ('Obsah', {
            'fields': ('title', 'description', 'type', 'icon')
        }),
        ('Čas a místo', {
            'fields': ('date', 'time', 'location'),
        }),
        ('Příloha', {
            'fields': ('attachment', 'attachment_name', 'attachment_size'),
        }),
    )

    @admin.display(description='Ikona')
    def icon_preview(self, obj):
        """Zobrazí živý náhled ikony ve výpisu příspěvků."""
        return format_html(
            '<span style="font-family:\'Material Symbols Outlined\';'
            'font-size:1.4rem;vertical-align:middle;" '
            'title="{name}">{name}</span>',
            name=obj.icon,
        )

    class Media:
        # Načte Material Symbols do admin stránky pro náhled ikon
        css = {
            'all': (
                'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined'
                ':wght,FILL@400,0&display=swap',
            )
        }
