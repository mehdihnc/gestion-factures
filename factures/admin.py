from django.contrib import admin
from .models import Facture, Categorie, Client

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'montant', 'est_payee', 'categorie')
    list_filter = ('client', 'est_payee', 'categorie')
    search_fields = ('numero', 'client__nom')
    actions = ['marquer_comme_payees']

    def marquer_comme_payees(self, request, queryset):
        updated = queryset.update(est_payee=True)
        if updated == 1:
            message = '1 facture a été marquée comme payée.'
        else:
            message = f'{updated} factures ont été marquées comme payées.'
        self.message_user(request, message)
    marquer_comme_payees.short_description = "Marquer les factures sélectionnées comme payées"

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone')
    search_fields = ('nom', 'email')
