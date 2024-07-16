from django import forms
from .models import Livro
from django.contrib.auth.models import User

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'isbn']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirme a Senha")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")
        return password_confirm