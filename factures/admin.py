from django.contrib import admin
from .models import Facture, Categorie

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'date_creation', 'categorie', 'montant', 'est_payee']
    list_filter = ['est_payee', 'categorie', 'date_creation']
    search_fields = ['numero', 'categorie__nom']
    actions = ['marquer_comme_payee']

    def marquer_comme_payee(self, request, queryset):
        queryset.update(est_payee=True)
        self.message_user(request, f"{queryset.count()} factures ont été marquées comme payées.")
    marquer_comme_payee.short_description = "Marquer les factures sélectionnées comme payées"

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']
