from Tabook_models.models import Customer, Restaurant, Review
from django import forms


class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class RestaurantCreationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'

class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
