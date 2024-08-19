from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.Home_principal, name="Home_principale"),
    path("Connect", Connect.as_view(), name="connect"),
    path("IndexApp", views.Index_client, name="IndexApp"),
    path("Alerte/", views.Demand_conn, name="Demande"),
    path("Proprietaire-rendez-vous/", views.RdvProp, name="rdv_prop"),
    path('rendez-vousProp/', liste_rendez_vous, name='liste_rendez_vous'),
    path("UserAvis/", views.Aviss, name="avis"),
    path("UserRdv/", views.Rdv, name="rdv"),
    path("rendez-vous/", views.enregistrer_rendez_vous, name="enregistrer_rendez_vous"),
    path('habitats/', views.liste_habitats, name='liste_habitats'),
    path("home", Home.as_view(), name="home"),
    path('enregistrer-habitat/', enregistrer_habitat, name='enregistrer_habitat'),
    path("deleteFormateurAdmin/<int:id>", DeleteProprietaireAdmin.as_view(), name="deleteProproetaireAdmin"),
    path("updateFormateurAdmin/<int:id>", UpdateProprietaireAdmin.as_view(), name="updateProprietaireAdmin"),
    path("homeFormateur", HomeProprietaire.as_view(), name="homeProprietaire"),
    path("deleteFormation/<int:id>", DeleteHabitat.as_view(), name="deleteHabitat"),
    path("detailHabitat/<int:id>", DetailHabitat.as_view(), name="detailHabitat"),
    path("register", Register.as_view(), name="register"),
    path("homeApprenant", HomeClient.as_view(), name="homeClient"),
    path("formationView/<int:id>", HabitatView.as_view(), name="habitatView"),
    path("disconnect", Disconnect.as_view(), name="disconnect")
]