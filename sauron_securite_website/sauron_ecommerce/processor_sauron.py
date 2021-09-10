from sauron_ecommerce.models import Categorie, SousCategorie


def user(request):
    categories = Categorie.objects.all()
    if hasattr(request, 'user'):
        return {'user':request.user,'categories':categories }
    return {}
def categorie(request):
    categories = Categorie.objects.all()
    return {'categories': categories}
def souscategorie(request):
    souscategories = SousCategorie.objects.all()
    return {'souscategories': souscategories}