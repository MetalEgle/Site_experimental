from django import forms
from .models import Product


class NameForm(forms.Form):
    name = forms.CharField( max_length=50)
    category = forms.CharField(min_length=1)
    price = forms.IntegerField(min_value=1)
    body = forms.ChoiceField(
        choices=Product.BODY_CHOICES,
        label="Кузов",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    image = forms.ImageField(
        required=False,
        label="Фото автомобиля",
        widget=forms.ClearableFileInput(attrs={"accept": "image/*"}),
    )


class SearchForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=False,
        label="Модель или марка",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Например, Aventador или Lamborghini",
                "aria-label": "Название модели или марка",
            }
        ),
    )
    body_types = forms.MultipleChoiceField(
        choices=Product.BODY_CHOICES,
        required=False,
        label="Кузов",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "body-filter-options"}),
    )