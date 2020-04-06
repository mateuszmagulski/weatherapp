from django.test import TestCase, Client
from django.urls import reverse

from weather.models import City


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.city = City.objects.create(
            name="Gdynia"
        )
        self.delete_city_url = reverse("delete_city", args=[1])


    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "weather/weather.html")
    
    def test_index_add_city_POST(self):
        response = self.client.post(self.index_url, {
            "name":"sopot"
        })
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(City.objects.count(), 2)

    def test_index_add_city_POST_existing_city(self):
        response = self.client.post(self.index_url, {
            "name":"gdynia"
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(City.objects.count(), 1)

    def test_index_add_city_POST_no_data(self):
        response = self.client.post(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(City.objects.count(), 1)

    def test_delete_city_GET(self):
        response = self.client.get(self.delete_city_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(City.objects.count(), 0)