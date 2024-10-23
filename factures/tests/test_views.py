from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from factures.models import Facture, Client, Categorie
from decimal import Decimal

class FactureViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client_obj = Client.objects.create(
            user=self.user,
            nom='Test Client',
            email='test@example.com',
            telephone='0123456789'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        
        self.categorie = Categorie.objects.create(nom='Test Categorie')
        self.test_client = TestClient()

    def test_liste_factures_client_voit_ses_factures(self):
        """Test qu'un client ne voit que ses propres factures"""
        autre_user = User.objects.create_user(username='autre', password='12345')
        autre_client = Client.objects.create(
            user=autre_user,
            nom='Autre Client',
            email='autre@example.com'
        )
        
        Facture.objects.create(
            numero='TEST-001',
            client=self.client_obj,
            categorie=self.categorie,
            montant=Decimal('100.00')
        )
        Facture.objects.create(
            numero='TEST-002',
            client=autre_client,
            categorie=self.categorie,
            montant=Decimal('200.00')
        )

        self.test_client.login(username='testuser', password='12345')
        response = self.test_client.get(reverse('liste_factures'))
        
        self.assertEqual(len(response.context['factures']), 1)
        self.assertEqual(response.context['factures'][0].numero, 'TEST-001')

    def test_creation_facture_sans_categorie(self):
        """Test la création d'une facture sans catégorie"""
        self.test_client.login(username='testuser', password='12345')
        response = self.test_client.post(reverse('creer_facture'), {
            'numero': 'TEST-003',
            'montant': '300.00',
            'est_payee': False
        })
        
        facture = Facture.objects.get(numero='TEST-003')
        self.assertEqual(facture.categorie.nom, 'Autres')
        self.assertEqual(response.status_code, 302)

    def test_modification_facture_autre_client(self):
        """Test qu'un client ne peut pas modifier la facture d'un autre client"""
        autre_user = User.objects.create_user(username='autre', password='12345')
        autre_client = Client.objects.create(
            user=autre_user,
            nom='Autre Client',
            email='autre@example.com'
        )
        facture = Facture.objects.create(
            numero='TEST-004',
            client=autre_client,
            categorie=self.categorie,
            montant=Decimal('400.00')
        )

        self.test_client.login(username='testuser', password='12345')
        response = self.test_client.post(
            reverse('modifier_facture', kwargs={'pk': facture.pk}),
            {'numero': 'TEST-004-MOD', 'montant': '500.00'}
        )
        
        self.assertEqual(response.status_code, 302)
        facture.refresh_from_db()
        self.assertEqual(facture.numero, 'TEST-004') 

