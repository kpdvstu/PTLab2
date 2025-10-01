from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "password123")

    def test_admin_redirects_without_login(self):
        response = self.client.get("/admin/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log in")

    def test_admin_access_after_login(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Site administration")
