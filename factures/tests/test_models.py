from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from factures.models import Facture, Client, Categorie
from decimal import Decimal

class FactureModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client_obj = Client.objects.create(
            user=self.user,
            nom='Test Client',
            email='test@example.com',
            telephone='0123456789'
        )
        self.categorie = Categorie.objects.create(nom='Test Categorie')

    def test_creation_facture_avec_montant_negatif(self):
        """Test qu'une facture ne peut pas avoir un montant négatif"""
        with self.assertRaises(ValidationError):
            facture = Facture.objects.create(
                numero='TEST-001',
                client=self.client_obj,
                categorie=self.categorie,
                montant=Decimal('-100.00')
            )
            facture.full_clean()

    def test_categorie_autres_automatique(self):
        """Test que la catégorie 'Autres' est assignée automatiquement"""
        facture = Facture.objects.create(
            numero='TEST-002',
            client=self.client_obj,
            montant=Decimal('100.00')
        )
        self.assertEqual(facture.categorie.nom, 'Autres')

    def test_numero_facture_unique(self):
        """Test que deux factures ne peuvent pas avoir le même numéro"""
        Facture.objects.create(
            numero='TEST-003',
            client=self.client_obj,
            categorie=self.categorie,
            montant=Decimal('100.00')
        )
        with self.assertRaises(ValidationError):
            facture2 = Facture.objects.create(
                numero='TEST-003',
                client=self.client_obj,
                categorie=self.categorie,
                montant=Decimal('200.00')
            )
            facture2.full_clean()
