from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = "Site d'administration de GestCaisse"
admin.site.register(Employee)
admin.site.register(Caisse)
admin.site.register(Tier)
admin.site.register(CompteG)
admin.site.register(Categorie)
admin.site.register(CompteTier)
admin.site.register(Operation)
admin.site.register(VarSoldeCaisse)
admin.site.register(EmployeCaisse)
admin.site.register(EcritureComptable)