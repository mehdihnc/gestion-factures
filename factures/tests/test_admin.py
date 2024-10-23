from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from factures.models import Facture, Client as ClientModel, Categorie
from decimal import Decimal

class AdminActionsTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        
        self.client_user = User.objects.create_user(username='client', password='12345')
        self.client_obj = ClientModel.objects.create(
            user=self.client_user,
            nom='Test Client',
            email='test@example.com'
        )
        self.categorie = Categorie.objects.create(nom='Test Categorie')
        
        for i in range(3):
            Facture.objects.create(
                numero=f'TEST-00{i}',
                client=self.client_obj,
                categorie=self.categorie,
                montant=Decimal(f'{100 * (i+1)}.00'),
                est_payee=False
            )
        
        self.client = Client()

    def test_marquer_factures_comme_payees(self):
        """Test l'action admin pour marquer plusieurs factures comme payées"""
        self.client.login(username='admin', password='admin123')
        
        factures = Facture.objects.all()
        facture_ids = list(factures.values_list('id', flat=True))
        
        response = self.client.post(reverse('admin:factures_facture_changelist'), {
            'action': 'marquer_comme_payees',
            '_selected_action': facture_ids,
        })
        
        self.assertEqual(Facture.objects.filter(est_payee=True).count(), 3)

    def test_filtre_par_client(self):
        """Test le filtre admin par client"""
        autre_client = ClientModel.objects.create(
            user=User.objects.create_user(username='autre', password='12345'),
            nom='Autre Client',
            email='autre@example.com'
        )
        Facture.objects.create(
            numero='AUTRE-001',
            client=autre_client,
            categorie=self.categorie,
            montant=Decimal('1000.00')
        )

        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(f"/admin/factures/facture/?client__id__exact={self.client_obj.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cl'].result_list), 3)

