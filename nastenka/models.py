from django.db import models


class Post(models.Model):
    TYPE_URGENT = 'urgent'
    TYPE_INFO = 'info'
    TYPE_NOTICE = 'notice'
    TYPE_EVENT = 'event'

    POST_TYPES = [
        (TYPE_URGENT, 'Havarijní'),
        (TYPE_INFO, 'Informace'),
        (TYPE_NOTICE, 'Oznámení'),
        (TYPE_EVENT, 'Akce'),
    ]

    # Výběr ikon z Material Symbols – seřazeno po kategoriích
    ICON_CHOICES = [
        ('Havarijní', [
            ('emergency_home',      'Nouzová situace v domě'),
            ('warning',             'Varování'),
            ('water_damage',        'Poškození vodou'),
            ('plumbing',            'Instalatérství / voda'),
            ('electrical_services', 'Elektroinstalace'),
            ('local_fire_department','Požár / havarijní'),
        ]),
        ('Informace', [
            ('info',                'Informace (obecná)'),
            ('lightbulb',           'Tip / doporučení'),
            ('announcement',        'Oznámení'),
            ('campaign',            'Důležitá zpráva'),
            ('payments',            'Platby / finance'),
            ('account_balance',     'Bankovní / hospodaření'),
        ]),
        ('Oznámení / Údržba', [
            ('construction',        'Stavba / rekonstrukce'),
            ('build',               'Oprava / údržba'),
            ('handyman',            'Řemeslné práce'),
            ('delete_sweep',        'Úklid / odvoz odpadu'),
            ('elevator',            'Výtah'),
            ('lock',                'Zámek / přístup'),
        ]),
        ('Akce / Schůze', [
            ('event',               'Akce'),
            ('calendar_month',      'Termín / kalendář'),
            ('meeting_room',        'Schůze / shromáždění'),
            ('gavel',               'Hlasování / usnesení'),
            ('description',         'Dokument / zápis'),
            ('groups',              'Setkání obyvatel'),
        ]),
    ]

    title = models.CharField(max_length=200, verbose_name='Název')
    description = models.TextField(verbose_name='Popis')
    type = models.CharField(max_length=20, choices=POST_TYPES, default=TYPE_INFO, verbose_name='Typ')
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='info',
        verbose_name='Ikona',
    )
    date = models.CharField(max_length=100, blank=True, verbose_name='Datum')
    time = models.CharField(max_length=100, blank=True, verbose_name='Čas')
    location = models.CharField(max_length=200, blank=True, verbose_name='Místo')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name='Příloha')
    attachment_name = models.CharField(max_length=200, blank=True, verbose_name='Název přílohy')
    attachment_size = models.CharField(max_length=50, blank=True, verbose_name='Velikost přílohy')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Příspěvek'
        verbose_name_plural = 'Příspěvky'

    def __str__(self):
        return self.title
