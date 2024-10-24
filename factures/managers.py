from django.db import models
from django.db.models import Q, Sum
from decimal import Decimal

class FactureQuerySet(models.QuerySet):
    def payees(self):
        """Retourne les factures payées"""
        return self.filter(est_payee=True)

    def non_payees(self):
        """Retourne les factures non payées"""
        return self.filter(est_payee=False)

    def par_client(self, client):
        """Retourne les factures d'un client spécifique"""
        return self.filter(client=client)

    def montant_superieur_a(self, montant):
        """Retourne les factures avec un montant supérieur à la valeur donnée"""
        return self.filter(montant__gt=Decimal(str(montant)))

    def recherche(self, terme):
        """Recherche dans les numéros de facture et noms de clients"""
        return self.filter(
            Q(numero__icontains=terme) |
            Q(client__nom__icontains=terme)
        )

class FactureManager(models.Manager):
    def get_queryset(self):
        return FactureQuerySet(self.model, using=self._db)

    def creer_facture(self, numero, client, montant, **kwargs):
        """Crée une nouvelle facture avec validation"""
        from .models import Categorie
        categorie = kwargs.get('categorie')
        if not categorie:
            categorie, _ = Categorie.objects.get_or_create(nom="Autres")

        facture = self.model(
            numero=numero,
            client=client,
            categorie=categorie,
            montant=Decimal(str(montant)),
            est_payee=kwargs.get('est_payee', False)
        )
        facture.full_clean()
        facture.save()
        return facture

    def total_non_payees(self):
        """Retourne le montant total des factures non payées"""
        return self.get_queryset().non_payees().aggregate(
            total=models.Sum('montant')
        )['total'] or Decimal('0')
