import pycountry
import datetime

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator

current_year = datetime.datetime.now().year

phone_validator = RegexValidator(
    regex=r'^\+?\d{8,15}$',
    message="Le numéro de téléphone doit contenir entre 8 et 15 chiffres, avec éventuellement un + au début."
)

LANGUAGES_CHOICES = sorted(
    [
        (lang.alpha_2, lang.name)
        for lang in pycountry.languages
        if hasattr(lang, 'alpha_2')
    ],
    key=lambda x: x[1]  # tri par nom de langue
)

ICONE_CHOICES = [
    ("book", "Livre"),
    ("flask", "Science"),
    ("hat-wizard", "Fantastique"),
    ("landmark", "Histoire"),
    ("brain", "Philosophie"),
    ("feather-alt", "Poésie"),
    ("rocket", "Science-Fiction"),
    ("child", "Jeunesse"),
    ("palette", "Art"),
    ("music", "Musique"),
    ("futbol", "Sport"),
    ("utensils", "Cuisine"),
    ("globe", "Géographie"),
    ("user-tie", "Biographie"),
    ("heart", "Romance"),
    ("users", "Social"),
]

STATUS_CHOICES = [
    ("active","En Cours"),
    ("late","En Retard"),
    ("returned","Retourné"),
]

# Create your models here.
class Ecole(models.Model):
    nom = models.CharField(max_length=50,null=False)

    
class Etudiant(models.Model):
    matricule = models.CharField(max_length=12,primary_key=True,unique=True)
    nom = models.CharField(max_length=50,null=False)
    prenoms = models.CharField(max_length=150,null=False)
    dateNaiss = models.DateField()
    telephone = models.CharField(max_length=20,validators=[phone_validator],null=False)
    emailPers = models.CharField(max_length=50, null=False)
    emailInst = models.CharField(max_length=50, null=False)
    numChambre = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    ecole = models.ForeignKey(Ecole,on_delete=models.CASCADE)

    def active_loans(self):
        emprunts = Emprunter.objects.filter(etudiant=self).count()

        return emprunts
    
    def __str__(self):
        return f"{self.nom} {self.prenoms} - {self.numChambre} - {self.matricule}"

class Auteur(models.Model):
    nom_complet = models.CharField(max_length=150,null=False)

class Editeur(models.Model):
    nom = models.CharField(max_length=200,null=False)

class Categorie(models.Model):
    nom = models.CharField(max_length=40,null=False)
    description = models.TextField()
    icone = models.CharField(max_length=50, choices=ICONE_CHOICES)
    couleur = models.CharField(max_length=10, null=False)
    slug_url = models.SlugField(max_length=100, blank=True, unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Génère automatiquement un slug si vide
        if not self.slug_url:
            self.slug_url = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
    
    # ✅ Méthode pour récupérer les livres de cette catégorie
    def livres(self):
        return self.livre_set.count()

class Livre(models.Model):
    isbn = models.CharField(max_length=10, null=False)
    titre = models.CharField(max_length=100, null=False)
    langue = models.CharField(max_length=2, choices=LANGUAGES_CHOICES)
    quantite = models.SmallIntegerField(default=1)
    nbre_pages = models.SmallIntegerField()
    annee_publication = models.IntegerField(
        validators=[
            MinValueValidator(1400),          # éviter les années aberrantes
            MaxValueValidator(current_year)   # pas de date dans le futur
        ],
        null=True,
        blank=True
    )
    emplacement = models.CharField(max_length=200,null=True,blank=True)
    resume = models.TextField(null=True,blank=True)
    editeur = models.ForeignKey(Editeur,on_delete=models.CASCADE)
    auteur = models.ForeignKey(Auteur,on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie,on_delete=models.CASCADE)

    def is_available(self):
        emprunts = Emprunter.objects.filter(
            livre=self,
            status="active"
        ).count()

        return (self.quantite - emprunts) > 0
    
    def available_quantity(self):
        emprunts = Emprunter.objects.filter(
            livre=self,
            status="active"
        ).count()

        return self.quantite - emprunts
    
    def __str__(self):
        return f"{self.isbn} - {self.titre} - {self.quantite} - {self.emplacement}"

class Filiere(models.Model):
    nom = models.CharField(max_length=50,null=False)
    domaine = models.CharField(max_length=150,null=False)

class Emprunter(models.Model):
    dateEmprunt = models.DateField()
    dateRetourPrevu = models.DateField()
    dateRetourEffectif = models.DateField()
    duree = models.TimeField()
    etudiant= models.ForeignKey(Etudiant,on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre,on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    etat_livre = models.CharField(max_length=50, null=True)
    observation =  models.CharField(max_length=20, null=True)
