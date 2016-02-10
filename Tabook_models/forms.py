from Tabook_models.models import User
from django import forms


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
