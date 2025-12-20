from django.utils import timezone
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator

from books.models import Categorie, Emprunter, Etudiant, Ecole, Editeur, Auteur, Livre,ICONE_CHOICES,LANGUAGES_CHOICES

# Authentification

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



# Dashboard

@login_required(login_url='signin')
def dash(request):

    all_book_count = 0
    for book in Livre.objects.all():
        all_book_count += book.available_quantity()

    recent_activities = []
    # Placeholder si aucune activité récente n'est trouvée
    activities_placeholder = [
        {"message": "Aucune activité récente", "date": ""}
    ]
    context = {
        "recent_activities": recent_activities,
        "activities_placeholder": activities_placeholder,
        "total_books": all_book_count,
        "total_users": Etudiant.objects.filter(is_active=True).count()
    }
    return render(request, 'dashboard.html', context)



# Gestion des livres

@login_required(login_url='signin')
def books_list(request):
    categories_active = Categorie.objects.filter(is_active=True)
    livres = Livre.objects.all()

    search = request.GET.get("search", "")
    category_id = request.GET.get("category", "")
    status = request.GET.get("status", "")

    if search:
        livres = livres.filter(
            Q(titre__icontains=search) |
            Q(isbn__icontains=search) |
            Q(auteur__nom_complet__icontains=search) |
            Q(editeur__nom__icontains=search)
        )

    if category_id:
        livres = livres.filter(categorie_id=category_id)

    if status == "available":
        livres = livres.filter(quantite__gte=1)

    elif status == "borrowed":
        livres = livres.filter(quantite__lt=1)

    paginator = Paginator(livres, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "books_list.html", {
        "books": page_obj,
        "categories": categories_active,
        "search_query": search,
        "selected_category": category_id,
        "selected_status": status,
        "page_obj": page_obj,
        "is_paginated": True,
    })

@login_required(login_url='signin')
def books_form(request, pk=None):
    # Mode modification si un ID est présent
    book = None
    if pk:
        book = get_object_or_404(Livre, pk=pk)
    
    if request.method == "POST":
        isbn = request.POST.get("isbn")
        titre = request.POST.get("title")
        langue = request.POST.get("language")
        quantite = request.POST.get("total_quantity")
        nbre_pages = request.POST.get("pages")
        annee_publication = request.POST.get("publication_year")
        emplacement = request.POST.get("location")
        resume = request.POST.get("description")
        editeur = request.POST.get("publisher")
        auteur = request.POST.get("author")
        categorie_id = request.POST.get("category")

        # Sélection ou création d'un éditeur
        editeur_obj, created = Editeur.objects.get_or_create(
            nom=editeur.upper()
        )

        # Sélection ou création d'un auteur
        auteur_obj, created = Auteur.objects.get_or_create(
            nom_complet=auteur.title()
        )

        categorie = get_object_or_404(Categorie, id=categorie_id)

        if book:
            # Modification
            book.titre = titre
            book.langue = langue
            book.quantite = quantite
            book.nbre_pages = nbre_pages
            book.annee_publication = annee_publication
            book.emplacement = emplacement
            book.resume = resume
            book.editeur = editeur_obj
            book.auteur = auteur_obj
            book.categorie = categorie
            book.save()
        else:
            # Création
            Livre.objects.create(
                isbn = isbn,
                titre = titre,
                langue = langue,
                quantite = quantite,
                nbre_pages = nbre_pages,
                annee_publication = annee_publication,
                emplacement = emplacement,
                resume = resume,
                editeur = editeur_obj,
                auteur = auteur_obj,
                categorie = categorie
            )
        return redirect("books_list")


    categories_active = Categorie.objects.filter(is_active=True)
    return render(request, 'books_form.html',{
        'book':book,
        'categories': categories_active,
        'languages': LANGUAGES_CHOICES
    })

@login_required(login_url='signin')
def books_delete(pk):
    book = get_object_or_404(Livre, pk=pk)
    book.delete()
    return redirect("books_list")



# Gestion des catégories

@login_required(login_url='signin')
def categories_list(request):
    categories = Categorie.objects.all()
    return render(request, "categories_list.html", {
        "categories": categories
    })

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
def categories_delete(pk):
    category = get_object_or_404(Categorie, pk=pk)
    category.delete()
    return redirect("categories_list")



# Gestion des Etudiants

@login_required(login_url='signin')
def users_list(request):
    users = Etudiant.objects.all()

    search = request.GET.get("search", "")

    if search:
        users = users.filter(
                Q(matricule__icontains=search) |
                Q(nom__icontains=search) |
                Q(emailInst__icontains=search) |
                Q(telephone__icontains=search)
            )
        
    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'users_list.html', {
        "users": page_obj,
        "search_query": search,
        "page_obj": page_obj,
        "is_paginated": True,
    })

@login_required(login_url='signin')
def users_form(request, pk=None):

    # Mode modification si un ID est présent
    user = None
    if pk:
        user = get_object_or_404(Etudiant, pk=pk)

    if request.method == "POST":
        matricule = request.POST.get("matricule")
        nom = request.POST.get("nom")
        prenoms = request.POST.get("prenoms")
        telephone = request.POST.get("telephone")
        emailInst = request.POST.get("emailInst")
        emailPers = request.POST.get("emailPers")
        ecole_nom = request.POST.get("ecole")
        dateNaiss = request.POST.get("dateNaiss")
        numChambre = request.POST.get("numChambre")
        is_active = request.POST.get("is_active") is not None

        # Sélection ou création d'une école
        ecole_obj, created = Ecole.objects.get_or_create(
            nom=ecole_nom.upper()
        )

        if user:
            # Modification
            user.matricule = matricule
            user.nom = nom
            user.prenoms = prenoms
            user.telephone = telephone
            user.emailInst = emailInst
            user.emailPers = emailPers
            user.dateNaiss = dateNaiss
            user.numChambre = numChambre
            user.ecole = ecole_obj
            user.is_active = is_active
            user.save()
        else:
            # Création
            Etudiant.objects.create(
                matricule = matricule,
                nom = nom,
                prenoms = prenoms,
                dateNaiss = dateNaiss,
                telephone = telephone,
                emailInst = emailInst,
                emailPers = emailPers,
                numChambre = numChambre,
                ecole = ecole_obj,
                is_active = is_active

            )
        return redirect("users_list")


    return render(request, 'users_form.html',{
        "user":user
    })

@login_required(login_url='signin')
def users_delete(request,pk):
    user = Etudiant.objects.get(pk=pk)
    user.delete()
    return redirect("users_list")



# Gestion des emprunts

@login_required(login_url='signin')
def loans_list(request):
    emprunts = Emprunter.objects.select_related(
        "etudiant",
        "livre",
        "livre__auteur"
    )

    search = request.GET.get("search", "")
    status = request.GET.get("status", "all")

    # 🔍 SEARCH
    if search:
        emprunts = emprunts.filter(
            Q(etudiant__nom__icontains=search) |
            Q(livre__titre__icontains=search) |
            Q(livre__auteur__nom_complet__icontains=search)
        )

    today = timezone.now().date()

    # 🎯 FILTER STATUS
    if status == "active":
        emprunts = emprunts.filter(
            dateRetourEffectif__isnull=True,
            dateRetourPrevu__gte=today
        )

    elif status == "late":
        emprunts = emprunts.filter(
            dateRetourEffectif__isnull=True,
            dateRetourPrevu__lt=today
        )

    elif status == "returned":
        emprunts = emprunts.filter(
            dateRetourEffectif__isnull=False
        )

    # 📄 PAGINATION
    paginator = Paginator(emprunts.order_by("-dateEmprunt"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "loans_list.html", {
        "loans": page_obj,
        "search_query": search,
        "status_filter": status,
        "page_obj": page_obj,
        "is_paginated": True,
    })

@login_required(login_url='signin')
def loans_form(request, pk=None):
    # Mode de visualisation
    loan = None
    if pk:
        loan = get_object_or_404(Emprunter,pk=pk)

    if request.method == "POST":
        etudiant_matri = request.POST.get("user")
        livre_isbn = request.POST.get("book")
        dateEmprunt = request.POST.get("borrow_date")
        dateRetourPrevu = request.POST.get("due_date")
        observation = request.POST.get("notes")

        etudiant = get_object_or_404(Etudiant, matricule=etudiant_matri)
        livre = get_object_or_404(Livre, isbn=livre_isbn)

        if not loan:
            # Création
            Emprunter.objects.create(
                etudiant = etudiant,
                livre = livre,
                dateEmprunt = dateEmprunt,
                dateRetourPrevu = dateRetourPrevu,
                observation = observation,
                status = "active"
            )

        return redirect("loans_list")

    context = {
        "loan":loan,
        'today': timezone.now().date(),
        'available_books': Livre.disponibles(),
        "users": Etudiant.objects.filter(is_active=True)
    }
    return render(request, 'loans_form.html', context)

@login_required(login_url='signin')
def returns_form(request, pk=None):
    return render(request, 'returns_form.html')

@login_required(login_url='signin')
def loans_delete(request, pk):
    loan = get_object_or_404(Emprunter, pk=pk)
    loan.delete()
    return redirect("loans_list")



# Gestion du profil des utilisateur

@login_required(login_url='signin')
def history(request):
    return render(request, 'history.html')

@login_required(login_url='signin')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='signin')
def history_export(request):
    pass

@login_required(login_url='signin')
def change_password(request):
    pass
