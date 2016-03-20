from .models import Customer, Restaurant, Review, Reservation
from django import forms


# TODO: override to check for duplicate usernames

class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate(self):
        pass


class RestaurantCreationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate(self):
        pass


class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'


class ReservationCreationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
