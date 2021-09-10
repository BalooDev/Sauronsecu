from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import ValueRange
from django.db.models.fields import BooleanField, CharField, DateTimeField, EmailField, IntegerField
from django.urls import reverse # Cette fonction est utilisée pour formater les URL
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=200,default="")
    ville = models.CharField(max_length=50,default="Paris")
    code_postal = models.CharField(max_length=6,default="00000",help_text="Entrez votre code postal")
    pays = models.CharField(max_length=50,default="France")
    email_confirmed = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True,upload_to='sauron_ecommerce/static/profileImage', height_field=None, width_field=None, max_length=100,default="null")

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()




class Produit(models.Model):
    """Classe qui définit un produit du site web: sauron securite"""
    #champs de formulaire    
    RESOLUTION_CHOICES = (
    ("none","none"),
    ("1080","hd"),
    ("2160",'hd+'),
    ("4320","4k"),
    ("8640","8k")
    )
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100,help_text="nom du produit",unique=True)
    description = models.TextField(null=False,max_length=200,help_text="une description attractif du produit")
    prix = models.FloatField(null=False,help_text="le prix du produit en euro")
    date_ajout = models.DateTimeField()
    poids = models.FloatField(null=True,help_text="poids du produit en gramme")
    resolution = models.TextField(choices=RESOLUTION_CHOICES)
    image1 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image2 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image3 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image4 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image5 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    note = models.FloatField(null=True)
    souscategorie = models.ForeignKey('SousCategorie', on_delete=models.SET_NULL, null=True)


    class Meta:
        ordering = ['nom','date_ajout']
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.nom

    def get_absolute_url(self):
        """Cette fonction est requise pas Django, lorsque vous souhaitez détailler le contenu d'un objet."""
        return reverse('produit-detail', args=[str(self.id)])

class Categorie(models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire    
    id = models.AutoField(primary_key=True)
    nom = models.TextField(max_length=100,help_text="nom du produit")
    description = models.TextField(max_length=200,help_text="une description attractif du produit")
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,default=0)

    class Meta:
        ordering = ['nom',]
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.nom

class SousCategorie(models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire    
    id = models.AutoField(primary_key=True)
    nom = models.TextField(max_length=100,help_text="nom du produit")
    description = models.TextField(max_length=200,help_text="une description attractif du produit")
    categorie = models.ForeignKey("Categorie",on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,default=0)

    class Meta:
        ordering = ['nom',]
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.nom
class CommentaireManager(models.Manager):
    def create_commentaire(self,user_id,produitid,titre_com,contenu_com,note_com):
        commentaire = self.create(profile_id=user_id,produit_id=produitid,titre=titre_com,contenu=contenu_com,note=note_com)
        return commentaire

class Commentaire(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    titre = models.TextField(max_length=20,null=False,default="")
    contenu = models.TextField(max_length=500,null=False,default="")
    note = models.IntegerField(null=False,default=0)
    date = models.DateTimeField(auto_now_add=True,null=True)
    produit = models.ForeignKey("Produit",on_delete=models.SET_NULL, null=True)
    objects = CommentaireManager()
    class Meta:
        ordering = ['profile',]
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.id


class PanierManager(models.Manager):
    def create_panier(self,user_id):
        panier = self.create(profile_id=user_id)
        return panier

class Panier(models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire    
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    produitspanier = models.ManyToManyField(Produit,through='ProduitPanier')
    total = models.FloatField(null=True,default=0)
    objects = PanierManager()
    class Meta:
        ordering = ['total',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.id

from datetime import datetime

class ProduitPanierManager(models.Manager):
    def lier_produit_panier(self,produit, panier,qte):
        panier = self.create(produit_id=produit, panier_id=panier,quantite=qte)
        return panier
class ProduitPanier(models.Model):
    id = models.AutoField(primary_key=True)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    quantite = models.IntegerField(null=False,default=0)
    objects = ProduitPanierManager()
    class Meta:
        ordering = ['date_joined',]
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.date_joined)

class Commande(models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire    
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    panier = models.ForeignKey("Panier",on_delete=models.SET_NULL, null=True)
    payer = models.BooleanField(default=False)
    date_payer = models.DateTimeField()

    class Meta:
        ordering = ['date_payer',]
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.date_payer

class Stock (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire    
    id = models.AutoField(primary_key=True)
    produit = models.ForeignKey("Produit",on_delete=models.SET_NULL, null=True)
    quantite = models.IntegerField(help_text='Quantité de produit en stock')

    class Meta:
        ordering = ['id',]
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.id

class Paiement (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire    
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    commande = models.ForeignKey("Commande",on_delete=models.SET_NULL, null=True)
    etat = models.BooleanField(default=False,help_text="Paiement accepté ou pas")

    

    class Meta:
        ordering = ['id',]
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.id
