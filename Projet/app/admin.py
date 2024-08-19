from django.contrib import admin
from .models import *

admin.site.register([User, Proprietaire, Client, Habitat, RendezVous, Avis])