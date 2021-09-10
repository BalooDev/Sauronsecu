from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    adresse = forms.CharField(help_text="1 rue Thomas Sankara")
    code_postal = forms.CharField(help_text="269000")
    pays = forms.CharField(help_text="Belgique par exemple")
    birth_date = forms.DateField(help_text='Votre date de naissance ( jj/mm/aaaa )')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)