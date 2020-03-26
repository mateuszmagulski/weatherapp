from django.test import SimpleTestCase

from weather.forms import CityForm


class TestForms(SimpleTestCase):

    def test_city_form_valid_data(self):
        form = CityForm(data={
            "name":"Sopot"
        })

        self.assertTrue(form.is_valid())

    def test_city_form_no_data(self):
        form = CityForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)