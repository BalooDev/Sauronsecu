from sauron_ecommerce.processor_sauron import user
from django.http.response import HttpResponse
from sauron_ecommerce.forms import  ConnexionForm, UserForm
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from sauron_ecommerce.tokens import account_activation_token
# Create your views here.
from sauron_ecommerce.models import Produit, Categorie, ProduitPanier, ProduitPanierManager, Profile, SousCategorie, Panier, Commentaire
categories = Categorie.objects.all()
def index(request):
    """View function for home page of site."""
    commentaires=Commentaire.objects.all()[:3]
    
    # Generate counts of some of the main objects

    # Render the HTML template index.html with the data in the context variable
    return render(request,'index.html', context = {'user': request.user,'categories':categories,'commentaires':commentaires})


from django.views import generic
def produits(request):
    produit_list = Produit.objects.all()
    return render(request,'sauron_ecommerce/produit_list.html', context = {'produit_list': produit_list})

def produitsbycategorie(request,categorie):
    categorieid=categorie
    categ=Categorie.objects.get(id=categorieid)
    souscateglist=SousCategorie.objects.filter(categorie_id=categorieid)
    sclist=[]
    for scl in souscateglist:
        sclist.append(scl.id)
    produit_list = Produit.objects.all().filter(souscategorie_id__in=sclist)
    return render(request,'sauron_ecommerce/produit_list.html', context = {'produit_list': produit_list,'souscategorie':False,'categorieid':categorieid,'categorie':categ})

def produitsbysouscategorie(request,categorie,souscategorie):
    souscateg = SousCategorie.objects.get(id=souscategorie)
    produit_list = Produit.objects.all().filter(souscategorie_id=souscategorie)
    return render(request,'sauron_ecommerce/produit_list.html', context = {'produit_list': produit_list,'souscategorie':souscateg})

def produit(request,id):
    idproduit = id
    commentaires=Commentaire.objects.all().filter(produit_id=idproduit)
    produit = Produit.objects.get(id=idproduit)
    panier=""
    try:
        panier = Panier.objects.get(profile_id=request.user.id)
        idpanier = panier.id
    except:
        pass
    ppt=True
    try:
        produitpan = ProduitPanier.objects.get(produit=idproduit,panier=idpanier)
    except :
        ppt=False
    if request.method == "POST":
        quantite = request.POST['quantity']
        message=""
        if ppt:
            ProduitPanier.objects.filter(id=produitpan.id).update(

                quantite=quantite
            )
        else:
            ProduitPanier.objects.lier_produit_panier(idproduit,idpanier,quantite)

            Panier.objects.filter(id=idpanier).update(
                total= float(panier.total) + (float(quantite)*float(produit.prix))
            )
            message="Un article vient de s'imicer dans votre panier"
        return render(request,'sauron_ecommerce/produit.html', context = {'produit': produit,'idproduit':idproduit,'panier':panier,"message":message,"ppt":ppt,'commentaires':commentaires})
    else:
        return render(request,'sauron_ecommerce/produit.html', context = {'produit': produit,'idproduit':idproduit,'panier':panier,"message":"","ppt":ppt,'commentaires':commentaires})


def panier(request,id):
    panierid=id
    produit_list = ProduitPanier.objects.filter(panier=id)
    panier = Panier.objects.get(id=panierid)
    profile = Profile.objects.get(id=request.user.id)
    if not request.user.id==panier.profile_id:
        return redirect('index',)
    else:
        return render(request,'sauron_ecommerce/panier.html', context = {'produit_list': produit_list,'panier':panier,'profile':profile})

def panierdelete(request,id):
    produitid=id
    panierid = ProduitPanier.objects.get(id=produitid).panier_id
    produit = ProduitPanier.objects.get(id=produitid).produit_id
    newtotal = Panier.objects.get(id=panierid).total - (ProduitPanier.objects.get(id=produitid).quantite * Produit.objects.get(id=produit).prix)
    Panier.objects.filter(id=panierid).update(total=newtotal)
    ProduitPanier.objects.get(id=produitid).delete()
    return redirect('panier',id=panierid)

def panierupdate(request,id):
    produitid=id
    panierid = ProduitPanier.objects.get(id=produitid).panier_id
    produit = ProduitPanier.objects.get(id=produitid).produit_id
    newtotal = Panier.objects.get(id=panierid).total - (ProduitPanier.objects.get(id=produitid).quantite * Produit.objects.get(id=produit).prix) + (float(request.POST['qt']) * Produit.objects.get(id=produit).prix)
    Panier.objects.filter(id=panierid).update(total=newtotal)
    ProduitPanier.objects.filter(id=produitid).update(quantite=int(request.POST['qt']))
    return redirect('panier',id=panierid)

def profile(request,id):
    profileid=id
    if not request.user.id==id:
        return redirect('index')
    profile = Profile.objects.get(id=profileid)
    if request.method == "POST":
        Profile.objects.filter(id=request.user.id).update(adresse=request.POST['adresse'],code_postal=request.POST['codepostal'],ville=request.POST['ville'],pays=request.POST['pays'])
        User.objects.filter(id=request.user.id).update(first_name=request.POST['prenom'],last_name=request.POST['nom']) 
        return render(request,'sauron_ecommerce/profile.html', context = {'profile':profile})
    else:
        return render(request,'sauron_ecommerce/profile.html', context = {'profile':profile})



def commentaire(request):

    if request.method == "POST":
        Commentaire.objects.create_commentaire(request.user.id,request.POST['idproduit'],request.POST['titre'],request.POST['contenu'],request.POST['note'])
        return render(request,'sauron_ecommerce/commentaireAdd.html', context = {'idproduit':request.POST['idproduit']})
    else:
        form = ConnexionForm()
    redirect('produits')

def commentairedelete(request,id):
    commentaireid=id
    produitid = Commentaire.objects.get(id=commentaireid).produit_id
    Commentaire.objects.get(id=commentaireid).delete()
    return redirect('produit',id=produitid)

from django.contrib.auth import logout
from django.shortcuts import render
from django.urls import reverse
    
def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db() 
            user.is_active = False
            user.profile.birth_date = user_form.cleaned_data.get('birth_date')
            user.profile.adresse = user_form.cleaned_data.get('adresse')
            user.profile.pays = user_form.cleaned_data.get('pays')
            user.profile.code_postal = user_form.cleaned_data.get('code_postal')
            user.save()
            Panier.objects.create_panier(user.id)
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        user_form = UserForm()
    return render(request, 'signup.html', {'user_form': user_form,'categories':categories})

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from sauron_ecommerce.tokens import account_activation_token

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

from django.contrib.auth import authenticate, login
