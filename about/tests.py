from django.test import TestCase
from django.urls import reverse

from .forms import NameForm
from .models import Product


class ProductBodyTests(TestCase):
    def test_add_product_form_requires_a_valid_body_choice(self):
        form_data = {
            "name": "City Car",
            "category": "Family",
            "price": 25000,
            "body": "SUV",
        }

        self.assertTrue(NameForm(data=form_data).is_valid())

        form_data["body"] = "Truck"
        self.assertFalse(NameForm(data=form_data).is_valid())

    def test_add_product_saves_selected_body(self):
        response = self.client.post(
            reverse("add_product"),
            {
                "name": "City Car",
                "category": "Family",
                "price": 25000,
                "body": "Wagon",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.get().body, "Wagon")
        self.assertContains(response, "Автомобиль успешно добавлен!")

    def test_catalog_displays_product_body(self):
        Product.objects.create(
            name="City Car",
            category="Family",
            price=25000,
            body="Liftback",
        )

        response = self.client.get(reverse("about"))

        self.assertContains(response, "Liftback")

    def test_catalog_search_filters_by_model_name(self):
        Product.objects.create(name="City Car", category="Family", price=25000, body="Sedan")
        Product.objects.create(name="Roadster", category="Sport", price=40000, body="Coupe")

        response = self.client.get(reverse("about"), {"name": "city"})

        self.assertContains(response, "City Car")
        self.assertNotContains(response, "Roadster")

    def test_catalog_search_filters_by_category(self):
        Product.objects.create(
            name="Aventador",
            category="Lamborghini",
            price=250000,
            body="Coupe",
        )
        Product.objects.create(
            name="911",
            category="Porsche",
            price=120000,
            body="Coupe",
        )

        response = self.client.get(reverse("about"), {"name": "Lamborghini"})

        self.assertContains(response, "<h2>Aventador</h2>")
        self.assertNotContains(response, "<h2>911</h2>")

    def test_catalog_filters_by_multiple_body_types(self):
        Product.objects.create(name="City Car", category="Family", price=25000, body="Sedan")
        Product.objects.create(name="Roadster", category="Sport", price=40000, body="Coupe")
        Product.objects.create(name="Touring", category="Family", price=30000, body="Wagon")

        response = self.client.get(
            reverse("about"),
            {"body_types": ["Coupe", "Wagon"]},
        )

        self.assertContains(response, "Roadster")
        self.assertContains(response, "Touring")
        self.assertNotContains(response, "<h2>City Car</h2>")

    def test_catalog_combines_name_and_body_filters(self):
        Product.objects.create(name="City Sedan", category="Family", price=25000, body="Sedan")
        Product.objects.create(name="City Coupe", category="Sport", price=40000, body="Coupe")

        response = self.client.get(
            reverse("about"),
            {"name": "City", "body_types": ["Coupe"]},
        )

        self.assertContains(response, "City Coupe")
        self.assertNotContains(response, "<h2>City Sedan</h2>")
