from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return self.nom

class Facture(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    date_creation = models.DateField(auto_now_add=True)
    categorie = models.ForeignKey('Categorie', on_delete=models.SET_NULL, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    est_payee = models.BooleanField(default=False)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Facture {self.numero}"

    def clean(self):
        if self.montant and self.montant < 0:
            raise ValidationError({'montant': 'Le montant ne peut pas être négatif.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.categorie:
            categorie_autres, _ = Categorie.objects.get_or_create(nom="Autres")
            self.categorie = categorie_autres
        super().save(*args, **kwargs)
