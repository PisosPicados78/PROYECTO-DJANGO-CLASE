from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
