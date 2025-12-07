from django.utils import timezone
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.text import slugify

from books.models import Categorie,ICONE_CHOICES

# Create your views here.

def signin(request):
    # Si l’utilisateur est déjà connecté → redirection
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Gestion du "remember me"
            if not remember:
                request.session.set_expiry(0)  # expire quand on ferme le navigateur

            messages.success(request, "Connexion réussie !")
            return redirect("dashboard")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('signin')

@login_required(login_url='signin')
def dash(request):
    recent_activities = []
    # Placeholder si aucune activité récente n'est trouvée
    activities_placeholder = [
        {"message": "Aucune activité récente", "date": ""}
    ]
    context = {
        "recent_activities": recent_activities,
        "activities_placeholder": activities_placeholder
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='signin')
def books_list(request):
    return render(request, 'books_list.html')

@login_required(login_url='signin')
def loans_list(request):
    return render(request, 'loans_list.html')

@login_required(login_url='signin')
def users_list(request):
    return render(request, 'users_list.html')

@login_required(login_url='signin')
def categories_list(request):
    categories = Categorie.objects.all()
    return render(request, "categories_list.html", {
        "categories": categories
    })

@login_required(login_url='signin')
def history(request):
    return render(request, 'history.html')

@login_required(login_url='signin')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='signin')
def loans_form(request):
    context = {
        'today': timezone.now().date()
    }
    return render(request, 'loans_form.html', context)

@login_required(login_url='signin')
def returns_form(request):
    return render(request, 'returns_form.html')

@login_required(login_url='signin')
def books_form(request):
    return render(request, 'books_form.html')

@login_required(login_url='signin')
def users_form(request):
    return render(request, 'users_form.html')

@login_required(login_url='signin')
def categories_form(request, pk=None):
    # Mode modification si un ID est présent
    category = None
    if pk:
        category = get_object_or_404(Categorie, pk=pk)

    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        icone = request.POST.get("icone")
        couleur = request.POST.get("couleur")
        active = request.POST.get("is_active") is not None

        if category:
            # Modification
            category.nom = nom
            category.description = description
            category.icone = icone
            category.couleur = couleur
            category.slug_url = slugify(nom)
            category.is_active = active
            category.save()
        else:
            # Création
            Categorie.objects.create(
                nom=nom,
                description=description,
                icone=icone,
                couleur=couleur,
                is_active=active,
                slug_url=slugify(nom)
            )

        return redirect("categories_list")

    return render(request, "categories_form.html", {
        "category": category,
        "ICONE_CHOICES": ICONE_CHOICES,
    })

@login_required(login_url='signin')
def categories_delete(request, pk):
    category = get_object_or_404(Categorie, pk=pk)
    category.delete()
    return redirect("categories_list")

@login_required(login_url='signin')
def history_export(request):
    pass

@login_required(login_url='signin')
def change_password(request):
    pass
