from django.db import models
from django.contrib.auth.models import AbstractUser

# Classe User modifiée
class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=False)
    number_phone = models.CharField(max_length=14, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "status"]
    
    def __str__(self):
        return self.username

# Classe pour les propriétaires
class Proprietaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

# Classe pour les clients
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

# Classe pour les habitats
class Habitat(models.Model):
    id = models.AutoField(primary_key=True)
    idProprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    avenue = models.CharField(max_length=255)
    quartier = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilite = models.BooleanField(default=True)
    localisation = models.CharField(max_length=255, default='https://maps.app.goo.gl/cxDy3WQex4ibrVXG9')
    images = models.ImageField(upload_to='habitats/')
    image_on = models.ImageField(default='static/image/maison-deux.jpg')
    image_to = models.ImageField(default='static/image/maison-deux.jpg')


    def __str__(self):
        return self.titre

# Classe pour les rendez-vous
class RendezVous(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rendez-vous le {self.date} pour {self.client.user.username} - Habitat: {self.habitat.titre}"

# Classe pour les avis
class Avis(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    commentaire = models.TextField()

    def __str__(self):
        return f"Avis de {self.client.user.username} pour {self.habitat.titre} le {self.date}"
