from django.test import TestCase, Client
from django.urls import reverse


class StaticPageTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        response = self.guest_client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        response = self.guest_client.get('/about/')
        self.assertTemplateUsed(response, 'static_pages/about.html')

    def test_about_url_accessible_by_its_name(self):
        response = self.guest_client.get(reverse('static_pages:about'))
        self.assertEqual(response.status_code, 200)

