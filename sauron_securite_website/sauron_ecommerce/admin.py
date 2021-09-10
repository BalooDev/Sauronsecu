from django.contrib.auth.models import User
from sauron_ecommerce.models import Categorie, Produit, Profile, SousCategorie, Panier
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

admin.site.register(Profile)

class ProduitAdmin(admin.ModelAdmin):
    list_display=('nom','description','prix','poids','souscategorie','resolution','date_ajout')
    fields=('nom','description','prix','poids','souscategorie','resolution','date_ajout',('image1','image2','image3'))

admin.site.register(Produit,ProduitAdmin)

class CategorieAdmin(admin.ModelAdmin):
    pass

admin.site.register(Categorie,CategorieAdmin)

class SousCategorieAdmin(admin.ModelAdmin):
    pass

admin.site.register(SousCategorie,SousCategorieAdmin)

class PanierAdmin(admin.ModelAdmin):
    pass

admin.site.register(Panier,PanierAdmin)