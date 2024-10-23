from django import forms
from .models import Facture, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone']

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['numero', 'categorie', 'montant', 'est_payee']
