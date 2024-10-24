from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Facture, Categorie, Client
from .forms import FactureForm, ClientForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username} ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/inscription.html', {'form': form})


def accueil(request):
    """Vue pour la page d'accueil."""
    return render(request, 'factures/base.html')


@login_required
def factures_par_categorie(request, categorie_id):
    """Vue pour afficher les factures liées à une catégorie spécifique."""
    categorie = get_object_or_404(Categorie, id=categorie_id)
    factures = Facture.objects.filter(categorie=categorie)
    return render(request, 'factures/factures_par_categorie.html', {'factures': factures, 'categorie': categorie})


@login_required
def liste_factures(request):
    # Vérifier si l'utilisateur est un client
    try:
        client = Client.objects.get(user=request.user)
        # Si c'est un client, ne montrer que ses factures
        factures = Facture.objects.filter(client=client)
        context = {
            'factures': factures,
            'client': client,
        }
    except Client.DoesNotExist:
        # Si c'est un admin, montrer toutes les factures avec le filtre client
        if request.user.is_staff:
            client_id = request.GET.get('client')
            factures = Facture.objects.all()
            if client_id:
                factures = factures.filter(client_id=client_id)
            clients = Client.objects.all()
            context = {
                'factures': factures,
                'clients': clients,
                'selected_client': client_id,
                'is_admin': True
            }
        else:
            factures = Facture.objects.none()
            context = {
                'factures': factures,
                'message': "Vous n'êtes pas encore enregistré comme client."
            }
    
    return render(request, 'factures/liste_factures.html', context)


@login_required
def liste_categories(request):
    """Vue pour afficher la liste des catégories. Accessible à tous les utilisateurs connectés."""
    categories = Categorie.objects.all()
    return render(request, 'factures/liste_categories.html', {'categories': categories})


@login_required
def detail_facture(request, pk):
    """Vue pour afficher les détails d'une facture."""
    facture = get_object_or_404(Facture, pk=pk)
    return render(request, 'factures/detail_facture.html', {'facture': facture})


@login_required
def creer_facture(request):
    print(f"Utilisateur connecté : {request.user.username}")  # Debug
    
    try:
        client = Client.objects.get(user=request.user)
        print(f"Client trouvé : {client.nom}")  # Debug
    except Client.DoesNotExist:
        print(f"Aucun client trouvé pour {request.user.username}")  # Debug
        messages.error(request, "Vous devez être enregistré comme client pour créer une facture.")
        return redirect('liste_factures')

    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            facture = form.save(commit=False)
            facture.client = client
            facture.save()
            messages.success(request, "Facture créée avec succès.")
            return redirect('liste_factures')
    else:
        form = FactureForm()

    return render(request, 'factures/creer_facture.html', {
        'form': form,
        'client': client
    })


@login_required
def modifier_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire de la facture ou un admin
    if not request.user.is_staff and facture.client.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette facture.")
        return redirect('liste_factures')

    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            messages.success(request, "La facture a été mise à jour avec succès.")
            return redirect('liste_factures')
    else:
        form = FactureForm(instance=facture)
        if not request.user.is_staff:
            form.fields['client'].widget.attrs['disabled'] = True
            form.fields['client'].widget.attrs['readonly'] = True

    return render(request, 'factures/modifier_facture.html', {'form': form, 'facture': facture})


@login_required
def supprimer_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire de la facture ou un admin
    if not request.user.is_staff and facture.client.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette facture.")
        return redirect('liste_factures')

    if request.method == 'POST':
        facture.delete()
        messages.success(request, "La facture a été supprimée avec succès.")
        return redirect('liste_factures')
    return render(request, 'factures/supprimer_facture.html', {'facture': facture})
