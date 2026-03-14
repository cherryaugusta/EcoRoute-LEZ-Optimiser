from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_endpoint_exists(self) -> None:
        url = reverse("health")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, [200, 503])
        body = resp.json()
        self.assertIn("status", body)
        self.assertIn("database", body)
        self.assertIn("redis", body)
