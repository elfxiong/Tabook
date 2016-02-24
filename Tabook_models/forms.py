from Tabook_models.models import Customer, Restaurant
from django import forms


class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class RestaurantCreationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'
