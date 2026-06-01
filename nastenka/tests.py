"""
Testy pro aplikaci nastenka – BD Kutná Hora.

Spuštění (lokálně bez Dockeru):
    python manage.py test --settings=bd_project.test_settings

Spuštění (v Dockeru):
    docker compose exec web python manage.py test
"""
from io import StringIO

from django.contrib.admin import site as admin_site
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post


# ---------------------------------------------------------------------------
# Model testy
# ---------------------------------------------------------------------------

class PostModelTest(TestCase):
    """Testy pro model Post."""

    def setUp(self):
        self.post = Post.objects.create(
            title='Testovací příspěvek',
            description='Popis testovacího příspěvku',
            type=Post.TYPE_INFO,
            icon='info',
        )

    def test_str_vraci_nazev(self):
        self.assertEqual(str(self.post), 'Testovací příspěvek')

    def test_vychozi_typ_je_info(self):
        post = Post.objects.create(title='Test', description='Popis')
        self.assertEqual(post.type, Post.TYPE_INFO)

    def test_vychozi_ikona_je_info(self):
        post = Post.objects.create(title='Test', description='Popis')
        self.assertEqual(post.icon, 'info')

    def test_razeni_nejnovejsi_prvni(self):
        novejsi = Post.objects.create(title='Novější', description='Popis')
        posts = list(Post.objects.all())
        self.assertEqual(posts[0], novejsi)
        self.assertEqual(posts[1], self.post)

    def test_vsechny_typy_prispevku(self):
        for hodnota, _ in Post.POST_TYPES:
            post = Post.objects.create(
                title=f'Test {hodnota}',
                description='Popis',
                type=hodnota,
            )
            self.assertEqual(post.type, hodnota)

    def test_get_type_display_havarijni(self):
        self.post.type = Post.TYPE_URGENT
        self.assertEqual(self.post.get_type_display(), 'Havarijní')

    def test_get_type_display_informace(self):
        self.post.type = Post.TYPE_INFO
        self.assertEqual(self.post.get_type_display(), 'Informace')

    def test_get_type_display_oznameni(self):
        self.post.type = Post.TYPE_NOTICE
        self.assertEqual(self.post.get_type_display(), 'Oznámení')

    def test_get_type_display_akce(self):
        self.post.type = Post.TYPE_EVENT
        self.assertEqual(self.post.get_type_display(), 'Akce')

    def test_volitelna_pole_jsou_prazdna_vychozi(self):
        post = Post.objects.create(title='Minimální', description='Popis')
        self.assertEqual(post.date, '')
        self.assertEqual(post.time, '')
        self.assertEqual(post.location, '')
        self.assertEqual(post.attachment_name, '')
        self.assertEqual(post.attachment_size, '')
        self.assertFalse(post.attachment)

    def test_casova_razitka_jsou_nastavena(self):
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)

    def test_verbose_name(self):
        self.assertEqual(Post._meta.verbose_name, 'Příspěvek')

    def test_verbose_name_plural(self):
        self.assertEqual(Post._meta.verbose_name_plural, 'Příspěvky')

    def test_konstanty_typu(self):
        self.assertEqual(Post.TYPE_URGENT, 'urgent')
        self.assertEqual(Post.TYPE_INFO, 'info')
        self.assertEqual(Post.TYPE_NOTICE, 'notice')
        self.assertEqual(Post.TYPE_EVENT, 'event')

    def test_icon_choices_existuji(self):
        """ICON_CHOICES je definován a neprázdný."""
        self.assertTrue(len(Post.ICON_CHOICES) > 0)

    def test_vsechny_icon_choices_jsou_validni_strings(self):
        """Každá hodnota v ICON_CHOICES je neprázdný string bez mezer."""
        for skupina, ikony in Post.ICON_CHOICES:
            for hodnota, popis in ikony:
                self.assertIsInstance(hodnota, str)
                self.assertTrue(len(hodnota) > 0)
                self.assertNotIn(' ', hodnota, msg=f'Ikona "{hodnota}" obsahuje mezeru – Material Symbols neakceptuje mezery')

    def test_vychozi_ikona_je_v_choices(self):
        """Výchozí ikona 'info' musí být v seznamu ICON_CHOICES."""
        vsechny_hodnoty = [v for _, skupina in Post.ICON_CHOICES for v, _ in skupina]
        self.assertIn('info', vsechny_hodnoty)

    def test_prispevek_se_vsemi_poli(self):
        post = Post.objects.create(
            title='Kompletní příspěvek',
            description='Kompletní popis',
            type=Post.TYPE_URGENT,
            icon='emergency',
            date='15. března 2025',
            time='08:00 – 16:00',
            location='Táborská 940/31',
            attachment_name='plan_opravy.pdf',
            attachment_size='840 KB',
        )
        self.assertEqual(post.title, 'Kompletní příspěvek')
        self.assertEqual(post.date, '15. března 2025')
        self.assertEqual(post.time, '08:00 – 16:00')
        self.assertEqual(post.location, 'Táborská 940/31')
        self.assertEqual(post.attachment_name, 'plan_opravy.pdf')
        self.assertEqual(post.attachment_size, '840 KB')


# ---------------------------------------------------------------------------
# View testy – Úvodní strana (index)
# ---------------------------------------------------------------------------

class IndexViewTest(TestCase):
    """Testy pro úvodní stranu."""

    def test_vraci_200(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_pouziva_spravnou_sablonu(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_aktivni_stranka_v_kontextu(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['active_page'], 'index')

    def test_pocet_prispevku_nula_bez_dat(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['recent_posts_count'], 0)

    def test_akce_se_nepocitaji_jako_nove(self):
        Post.objects.create(title='Akce', description='Popis', type=Post.TYPE_EVENT)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['recent_posts_count'], 0)

    def test_havarijni_se_pocita(self):
        Post.objects.create(title='Havárie', description='Popis', type=Post.TYPE_URGENT)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['recent_posts_count'], 1)

    def test_informace_se_pocita(self):
        Post.objects.create(title='Info', description='Popis', type=Post.TYPE_INFO)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['recent_posts_count'], 1)

    def test_oznameni_se_pocita(self):
        Post.objects.create(title='Oznámení', description='Popis', type=Post.TYPE_NOTICE)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['recent_posts_count'], 1)

    def test_smiseny_pocet_prispevku(self):
        Post.objects.create(title='P1', description='Popis', type=Post.TYPE_URGENT)
        Post.objects.create(title='P2', description='Popis', type=Post.TYPE_INFO)
        Post.objects.create(title='P3', description='Popis', type=Post.TYPE_NOTICE)
        Post.objects.create(title='Akce', description='Popis', type=Post.TYPE_EVENT)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['recent_posts_count'], 3)


# ---------------------------------------------------------------------------
# View testy – Nástěnka
# ---------------------------------------------------------------------------

class NastenkaViewTest(TestCase):
    """Testy pro nástěnku."""

    def setUp(self):
        self.post = Post.objects.create(
            title='Test Post',
            description='Test popis',
            type=Post.TYPE_INFO,
        )

    def test_vraci_200(self):
        response = self.client.get(reverse('nastenka'))
        self.assertEqual(response.status_code, 200)

    def test_pouziva_spravnou_sablonu(self):
        response = self.client.get(reverse('nastenka'))
        self.assertTemplateUsed(response, 'nastenka/nastenka.html')

    def test_aktivni_stranka_v_kontextu(self):
        response = self.client.get(reverse('nastenka'))
        self.assertEqual(response.context['active_page'], 'nastenka')

    def test_prispevky_v_kontextu(self):
        response = self.client.get(reverse('nastenka'))
        self.assertIn('posts', response.context)
        self.assertIn(self.post, response.context['posts'])

    def test_prazdna_nastenka(self):
        Post.objects.all().delete()
        response = self.client.get(reverse('nastenka'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 0)

    def test_prispevky_razeny_nejnovejsi_prvni(self):
        novejsi = Post.objects.create(title='Novější', description='Popis', type=Post.TYPE_NOTICE)
        response = self.client.get(reverse('nastenka'))
        posts = list(response.context['posts'])
        self.assertEqual(posts[0], novejsi)
        self.assertEqual(posts[1], self.post)

    def test_vsechny_typy_zobrazeny(self):
        for typ, _ in Post.POST_TYPES:
            Post.objects.create(title=f'Post {typ}', description='Popis', type=typ)
        response = self.client.get(reverse('nastenka'))
        # +1 za setUp post
        self.assertEqual(len(response.context['posts']), len(Post.POST_TYPES) + 1)


# ---------------------------------------------------------------------------
# View testy – Kontakty
# ---------------------------------------------------------------------------

class KontaktyViewTest(TestCase):
    """Testy pro stránku kontaktů."""

    def test_vraci_200(self):
        response = self.client.get(reverse('kontakty'))
        self.assertEqual(response.status_code, 200)

    def test_pouziva_spravnou_sablonu(self):
        response = self.client.get(reverse('kontakty'))
        self.assertTemplateUsed(response, 'kontakty.html')

    def test_aktivni_stranka_v_kontextu(self):
        response = self.client.get(reverse('kontakty'))
        self.assertEqual(response.context['active_page'], 'kontakty')


# ---------------------------------------------------------------------------
# View testy – Základní info
# ---------------------------------------------------------------------------

class ZakladniInfoViewTest(TestCase):
    """Testy pro stránku základních informací."""

    def test_vraci_200(self):
        response = self.client.get(reverse('zakladni-info'))
        self.assertEqual(response.status_code, 200)

    def test_pouziva_spravnou_sablonu(self):
        response = self.client.get(reverse('zakladni-info'))
        self.assertTemplateUsed(response, 'zakladni-info.html')

    def test_aktivni_stranka_v_kontextu(self):
        response = self.client.get(reverse('zakladni-info'))
        self.assertEqual(response.context['active_page'], 'zakladni-info')

    def test_nejnovejsi_prispevek_v_kontextu(self):
        post = Post.objects.create(title='Nejnovější', description='Popis', type=Post.TYPE_INFO)
        response = self.client.get(reverse('zakladni-info'))
        self.assertEqual(response.context['latest_post'], post)

    def test_latest_post_je_none_bez_prispevku(self):
        response = self.client.get(reverse('zakladni-info'))
        self.assertIsNone(response.context['latest_post'])

    def test_vraci_opravdu_nejnovejsi(self):
        Post.objects.create(title='Starší', description='Popis', type=Post.TYPE_INFO)
        novejsi = Post.objects.create(title='Novější', description='Popis', type=Post.TYPE_URGENT)
        response = self.client.get(reverse('zakladni-info'))
        self.assertEqual(response.context['latest_post'], novejsi)


# ---------------------------------------------------------------------------
# URL testy
# ---------------------------------------------------------------------------

class URLKonfiguraceTest(TestCase):
    """Testy pro URL konfiguraci."""

    def test_index_url(self):
        self.assertEqual(reverse('index'), '/')

    def test_nastenka_url(self):
        self.assertEqual(reverse('nastenka'), '/nastenka/')

    def test_kontakty_url(self):
        self.assertEqual(reverse('kontakty'), '/kontakty/')

    def test_zakladni_info_url(self):
        self.assertEqual(reverse('zakladni-info'), '/zakladni-info/')


# ---------------------------------------------------------------------------
# Admin testy
# ---------------------------------------------------------------------------

class AdminTest(TestCase):
    """Testy pro Django admin konfiguraci."""

    def test_post_je_registrovan_v_adminu(self):
        self.assertIn(Post, admin_site._registry)

    def test_admin_list_display(self):
        admin_instance = admin_site._registry[Post]
        for pole in ('title', 'type', 'icon_preview', 'date', 'created_at'):
            self.assertIn(pole, admin_instance.list_display)

    def test_admin_list_filter(self):
        admin_instance = admin_site._registry[Post]
        self.assertIn('type', admin_instance.list_filter)

    def test_admin_search_fields(self):
        admin_instance = admin_site._registry[Post]
        self.assertIn('title', admin_instance.search_fields)
        self.assertIn('description', admin_instance.search_fields)

    def test_admin_ordering(self):
        admin_instance = admin_site._registry[Post]
        self.assertEqual(admin_instance.ordering, ('-created_at',))


# ---------------------------------------------------------------------------
# Management command – import_posts
# ---------------------------------------------------------------------------

class ImportPostsCommandTest(TestCase):
    """Testy pro management command import_posts."""

    def test_import_vytvori_prispevky_z_posts_json(self):
        """Příkaz naimportuje data z posts.json v kořeni projektu."""
        out = StringIO()
        call_command('import_posts', stdout=out)
        vystup = out.getvalue()
        self.assertIn('Importováno', vystup)
        self.assertGreater(Post.objects.count(), 0)

    def test_import_je_idempotentni(self):
        """Opakované spuštění nevytváří duplicity."""
        out = StringIO()
        call_command('import_posts', stdout=out)
        pocet_po_prvnim = Post.objects.count()

        call_command('import_posts', stdout=out)
        pocet_po_druhem = Post.objects.count()

        self.assertEqual(pocet_po_prvnim, pocet_po_druhem)

    def test_import_chybejici_soubor(self):
        """Příkaz nevyhodí výjimku, pokud soubor neexistuje – jen vypíše chybu."""
        from unittest.mock import patch
        from pathlib import Path

        err = StringIO()
        with patch.object(Path, 'exists', return_value=False):
            # Nesmí vyhodit výjimku
            try:
                call_command('import_posts', stderr=err)
            except SystemExit:
                self.fail('import_posts vyhodil SystemExit při chybějícím souboru')
