from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

from centre_formation import settings
from .password_generator import generate_password
from django.core.mail import send_mail
from .models import *

def Home_principal(request):
    return render(request, 'app_auth/Home_principal.html')

def Index_client(request):
    
    list_of_habitats = Habitat.objects.all()
    count_habitats = Habitat.objects.all().count()
    
    context = {
        'list_of_habitats':list_of_habitats,
        'count_habitats':count_habitats,
    }
    return render(request, 'app/participant/index.html', context)

def Demand_conn(request):
    if request.user.is_authenticated:
        pass
    else:
        print('connectez vous !')
        return redirect('IndexApp')
        # return render(request, 'app/participants/alert.html')
    return render(request, 'app/participant/connexion.html')

def Aviss(request):
    return render(request, 'app/participant/avis.html')

def Rdv(request):
    return render(request, 'app/participant/rendezvous.html')

def RdvProp(request):
    rendez_vous = RendezVous.objects.all()
    context = {
        'rendez_vous':rendez_vous
    }

    return render(request, 'app/formateur/rendez_vous.html', context)

def liste_rendez_vous(request):
    rendez_vous = RendezVous.objects.all()  # Récupère tous les rendez-vous
    return render(request, 'app/formateur/rendez-vous.html', {'rendez_vous': rendez_vous})

def liste_habitats(request):
    habitats = Habitat.objects.all()  
    return render(request, 'votre_template.html', {'habitats': habitats})
class Connect(View):
    def get(self, request):
        template_name = "app_auth/connect.html"
        title = "Connexion"
        return render(request, template_name, {'title':title})
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if user.status == 'admin':
                return redirect('proprietaire')
            elif user.status == 'proprietaire':
                return redirect('homeProprietaire')
            elif user.status == 'client':
                return redirect('rdv')
        else:
            messages.error(request, "Informations incorrectes")
            return redirect('connect')

class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            template_name = "app/home.html"
            title = "Home"
            proprietaires = Proprietaire.objects.all()
            habitats = Habitat.objects.all()
            return render(request, template_name, {'title': title, 'proprietaires': proprietaires, 'habitats': habitats})
    
    def post(self, request):
        if request.user.is_authenticated:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            number_phone = request.POST.get('number_phone')
            email = request.POST.get('email')
            date_birth = request.POST.get('date_birth')
            sex = request.POST.get('sex')
            telephone = request.POST.get('telephone')
            adresse = request.POST.get('adresse')
            password = generate_password()
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email existe déjà !")
                return redirect('home')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    number_phone=number_phone,
                    email=email,
                    date_birth=date_birth,
                    sex=sex,
                    password=password,
                    status='proprietaire'
                )
                Proprietaire.objects.create(user=user, telephone=telephone, adresse=adresse)
                
                subject = "Bienvenue sur le site de gestion de logements"
                message = (f"Bonjour {username} - {first_name} - {last_name},\n\n"
                           f"Mot de passe : {password}\n"
                           f"\tVeuillez garder ces informations confidentielles.\n")
                sender = settings.EMAIL_HOST_USER
                recipient = [email]
                send_mail(subject, message, sender, recipient, fail_silently=True)
                messages.success(request, "L'enregistrement a réussi")
            
            return redirect('home')


def enregistrer_habitat(request):
    if request.method == "POST":
        titre = request.POST.get("title")
        avenue = request.POST.get("avenue")
        quartier = request.POST.get("quartier")
        commune = request.POST.get("commune")
        numero = request.POST.get("numero")
        description = request.POST.get("description")
        prix = request.POST.get("prix")
        disponibilite = request.POST.get("disponibilite").lower() in ['true', '1', 't', 'yes', 'y']
        image = request.FILES.get("image")

        # Récupérer le propriétaire lié à l'utilisateur connecté
        try:
            proprietaire = Proprietaire.objects.get(user=request.user)
        except Proprietaire.DoesNotExist:
            messages.error(request, "Vous n'êtes pas enregistré en tant que propriétaire.")
            return redirect("nom_de_la_vue_pour_afficher_le_formulaire")  # Rediriger vers la vue du formulaire

        # Créer un nouvel objet Habitat
        habitat = Habitat(
            idProprietaire=proprietaire,
            titre=titre,
            avenue=avenue,
            quartier=quartier,
            commune=commune,
            numero=numero,
            description=description,
            prix=prix,
            disponibilite=disponibilite,
            images=image
        )
        
        # Enregistrer l'objet dans la base de données
        habitat.save()

        messages.success(request, "Habitat enregistré avec succès.")
        return redirect('homeProprietaire')  # Rediriger vers une autre vue après enregistrement
    
    return render(request, "homeFormateur.html")

class UpdateProprietaireAdmin(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            title = "Modification Propriétaire"
            try:
                item = Proprietaire.objects.get(user__id=id)
            except Proprietaire.DoesNotExist:
                messages.error(request, "Propriétaire n'existe pas !")
                return redirect("home")
            return render(request, "app/update_formateur.html", {'title': title, 'item': item})

    def post(self, request, id):
        if request.user.is_authenticated:
            try:
                item = Proprietaire.objects.get(user__id=id)
            except Proprietaire.DoesNotExist:
                messages.error(request, "Propriétaire n'existe pas !")
                return redirect("home")
            item.user.username = request.POST.get('username')
            item.user.first_name = request.POST.get('first_name')
            item.user.last_name = request.POST.get('last_name')
            item.user.number_phone = request.POST.get('number_phone')
            item.user.email = request.POST.get('email')
            item.user.sex = request.POST.get('sex')
            item.user.date_birth = request.POST.get('date_birth')
            item.telephone = request.POST.get('telephone')
            item.adresse = request.POST.get('adresse')
            item.user.save()
            item.save()
            messages.success(request, "Modification réussie")
            return redirect("home")

class DeleteProprietaireAdmin(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                item = Proprietaire.objects.get(user__id=id)
                item.delete()
                messages.success(request, "Propriétaire a été supprimé avec succès.")
            except Proprietaire.DoesNotExist:
                messages.error(request, "Propriétaire n'a pas pu être supprimé. Il n'existe pas.")
            return redirect('home')

class HomeProprietaire(View):
    def get(self, request):
        if request.user.is_authenticated:
            template_name = "app/formateur/home_formateur.html"
            title = "Home"
            habitats = Habitat.objects.filter(idProprietaire__user=request.user)
            rendez_vous = RendezVous.objects.all()
            return render(request, template_name, {'title': title, 'habitats': habitats, 'rendez_vous':rendez_vous})
        return redirect('connect')
    
    def post(self, request):
        if request.user.is_authenticated:
            titre = request.POST.get('titre')
            avenue = request.POST.get('avenue')
            quartier = request.POST.get('quartier')
            commune = request.POST.get('commune')
            numero = request.POST.get('numero')
            description = request.POST.get('description')
            prix = request.POST.get('prix')
            disponibilite = request.POST.get('disponibilite') == 'on'
            images = request.FILES.get('images')
            Habitat.objects.create(
                idProprietaire=request.user.proprietaire,
                titre=titre,
                avenue=avenue,
                quartier=quartier,
                commune=commune,
                numero=numero,
                description=description,
                prix=prix,
                disponibilite=disponibilite,
                images=images
            )
            messages.success(request, "L'enregistrement a réussi")
            return redirect('homeProprietaire')
        return redirect('connect')

class DeleteHabitat(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                item = Habitat.objects.get(id=id)
                item.delete()
                messages.success(request, "Habitat a été supprimé avec succès.")
            except Habitat.DoesNotExist:
                messages.error(request, "Habitat n'a pas pu être supprimé. Il n'existe pas.")
            return redirect('homeProprietaire')

class DetailHabitat(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            title = "Détails Habitat"
            try:
                item = Habitat.objects.get(id=id)
                detail = Habitat.objects.all()
            except Habitat.DoesNotExist:
                messages.error(request, "Habitat n'existe pas !")
                return redirect("homeProprietaire")
            return render(request, "app/participant/Formation_v.html", {'title': title, 'item': item, 'detail':detail})

class Register(View):
    def get(self, request):
        template_name = "app/participant/register.html"
        title = "Register"
        return render(request, template_name, {'title': title})
    
    def post(self, request):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        number_phone = request.POST.get('number_phone')
        email = request.POST.get('email')
        date_birth = request.POST.get('date_birth')
        sex = request.POST.get('sex')
        address = request.POST.get('address')  # Notez le changement ici de 'adresse' à 'address'
        password = generate_password()

        # Vérification de l'existence de l'email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email existe déjà !")
            return redirect('register')
        else:
            # Création de l'utilisateur
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                number_phone=number_phone,
                email=email,
                date_birth=date_birth,
                sex=sex,
                password=password,
                status='client'  # Statut défini à 'client'
            )

            # Création du client associé
            Client.objects.create(user=user, telephone=number_phone, adresse=address)

            # Envoi de l'email de bienvenue
            subject = "Bienvenue sur le site de gestion de logements"
            message = (
                f"Bonjour {username} {first_name} {last_name},\n\n"
                f"Votre mot de passe est : {password}\n"
                f"Veuillez garder ces informations confidentielles.\n"
            )
            sender = settings.EMAIL_HOST_USER
            recipient = [email]
            send_mail(subject, message, sender, recipient, fail_silently=True)

            # Message de succès
            messages.success(request, "L'enregistrement a réussi, veuillez vérifier votre adresse email.")

        return redirect('connect')

class HomeClient(View):
    def get(self, request):
        if request.user.is_authenticated:
            template_name = "app/participant/home.html"
            title = "Client"
            habitats = Habitat.objects.all()
            return render(request, template_name, {'title': title, 'habitats': habitats})

class HabitatView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            template_name = "app/participant/habitat_v.html"
            title = "Détails Habitat"
            try:
                item = Habitat.objects.get(id=id)
            except Habitat.DoesNotExist:
                messages.error(request, "Habitat n'existe pas !")
                return redirect('homeClient')
            return render(request, template_name, {'title': title, 'item': item})

def enregistrer_rendez_vous(request):
    if request.method == "POST":
        habitat_concerne = request.POST.get('habitat_concerné')
        date = request.POST.get('date')
        client = request.user  # Assuming the user is a Client

        try:
            habitat = Habitat.objects.get(id=habitat_concerne)
            RendezVous.objects.create(
                date=date,
                client=client.client,  # assuming `Client` model is linked with `User` via a OneToOne relationship
                habitat=habitat
            )
            messages.success(request, "Rendez-vous enregistré avec succès.")
        except Habitat.DoesNotExist:
            messages.error(request, "L'habitat spécifié n'existe pas.")
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {e}")
        
        return redirect('rdv')  # Replace with your target URL

    return render(request, 'app/participant/index.html')  # Replace with the name of your template


class Disconnect(View):
    def get(self, request):
        logout(request)
        return redirect('connect')
