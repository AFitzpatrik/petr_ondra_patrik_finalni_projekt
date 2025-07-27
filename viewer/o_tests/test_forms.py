from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from viewer.models import Location, Type, City, Country
from viewer.forms import LocationModelForm, TypeModelForm


class ExtendedFormTests(TestCase):

    def setUp(self):
        # Vytvoření uživatele a přiřazení oprávnění pro testy
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user.user_permissions.add(Permission.objects.get(codename='add_location'))
        self.user.user_permissions.add(Permission.objects.get(codename='add_type'))

        # Vytvoření měst a zemí pro testy
        self.country = Country.objects.create(name="Česká republika")
        self.city = City.objects.create(name="Ostrava", country=self.country, zip_code="70030")

        # Přihlášení uživatele pro testování
        self.client.login(username='testuser', password='password')

    def test_add_location_with_duplicate_name(self):
        # Vytvoření první lokace
        location_1 = Location.objects.create(name="Sál A", address="Hlavní 123", city=self.city)

        # Snažíme se vytvořit druhou lokaci s duplicitním názvem
        response = self.client.post(reverse('location_create'), {
            'name': 'Sál A',  # Duplicitní název
            'address': 'Vedlejší 789',
            'city': self.city.id
        })

        # Očekáváme, že se objeví chyba (kód 200 místo přesměrování)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Location with this Name and Address already exists.')

    def test_add_location_with_permission(self):
        # Snažíme se přidat nový typ s oprávněním
        response = self.client.post(reverse('location_create'), {
            'name': 'Sál B',
            'address': 'Vedlejší 789',
            'city': self.city.id
        })

        # Ověřujeme, že lokace byla přidána
        self.assertTrue(Location.objects.filter(name="Sál B", address="Vedlejší 789").exists())
        self.assertEqual(response.status_code, 302)  # Očekáváme přesměrování po úspěšném přidání

    def test_add_location_without_permission(self):
        # Vytvoření nového uživatele bez oprávnění
        user_without_permission = User.objects.create_user(username='testuser2', password='password')
        self.client.login(username='testuser2', password='password')

        # Snažíme se přidat lokaci bez oprávnění
        response = self.client.post(reverse('location_create'), {
            'name': 'Sál C',
            'address': 'Druhá 456',
            'city': self.city.id
        })

        # Očekáváme, že uživatel bude přesměrován (chyba 403 Forbidden nebo přihlášení)
        self.assertEqual(response.status_code, 403)

    def test_add_type_with_duplicate_name(self):
        # Vytvoření prvního typu
        type_1 = Type.objects.create(name="Výstava")

        # Snažíme se vytvořit typ s duplicitním názvem
        response = self.client.post(reverse('type_create'), {
            'name': 'Výstava'  # Duplicitní název
        })

        # Očekáváme, že bude vrácena stránka s chybami formuláře (kód 200)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'Type with this Name already exists.')

    def test_add_type_with_permission(self):
        # Snažíme se přidat nový typ s oprávněním
        response = self.client.post(reverse('type_create'), {
            'name': 'Výstava'
        })

        # Ověřujeme, že typ byl přidán
        self.assertTrue(Type.objects.filter(name="Výstava").exists())
        self.assertEqual(response.status_code, 302)  # Očekáváme přesměrování po úspěšném přidání

    def test_add_type_without_permission(self):
        # Vytvoření nového uživatele bez oprávnění
        user_without_permission = User.objects.create_user(username='testuser2', password='password')
        self.client.login(username='testuser2', password='password')

        # Snažíme se přidat typ bez oprávnění
        response = self.client.post(reverse('type_create'), {
            'name': 'Výstava'
        })

        # Očekáváme, že uživatel bude přesměrován s chybou 403 (Forbidden)
        self.assertEqual(response.status_code, 403)

    def test_event_form_end_before_start(self):
        # Test pro kontrolu, že konec události nemůže být dříve než začátek
        response = self.client.post(reverse('event_create'), {
            'name': 'Test Event',
            'start_date_time': '2025-08-01T18:00',
            'end_date_time': '2025-08-01T16:00',  # Konec je před začátkem
            'event_image': '',
            'location': self.city.id,
            'capacity': 100
        })

        # Očekáváme, že se objeví chyba při nevalidních datech
        self.assertFormError(response, 'form', 'end_date_time', 'Konec události nemůže být dříve než začátek.')