import datetime

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


class ReservationForm(forms.Form):
    table = forms.IntegerField()
    # start_time = forms.DateTimeField(initial=datetime.datetime.now)  # no parenthesis
    # end_time = forms.DateTimeField(initial=datetime.datetime.now)
