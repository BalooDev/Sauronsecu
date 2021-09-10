from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produits/', views.produits, name='produits'),
    path('produits/categorie=<int:categorie>/', views.produitsbycategorie, name='produitsbycategorie'),
    path('produits/categorie=<int:categorie>/souscategorie=<int:souscategorie>', views.produitsbysouscategorie, name='produitsbysouscategorie'),
    path('commentaire/', views.commentaire, name='commentaire'),
    path('commentaire/<int:id>', views.commentairedelete, name='commentairedelete'),
    path('produit/<int:id>/', views.produit, name='produit'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('panier/<int:id>', views.panier, name='panier'),
    path('panier/delete/<int:id>', views.panierdelete, name='panierdelete'),
    path('panier/update/<int:id>', views.panierupdate, name='panierupdate'),
]