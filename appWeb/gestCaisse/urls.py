from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('index1/', views.index1 , name='index1'),  
    path('profile/', views.profile , name='profile'),   
    path('brouillards/', views.brouillards , name='brouillards'),
    path('operations/', views.operations , name='operations'),
    path('editOperation/', views.editOperation , name='editOperation'),
    
    path('employe/', views.employe , name='employe'),
    path('modifEmp/', views.modifEmp , name='modifEmp'),
    path('supprimerEmp/<int:emp_id>', views.supprimerEmp , name='supprimerEmp'),

    path('compteTiers/', views.compteTiers , name='compteTiers'),
    path('modifCompteTiers/', views.modifCompteTiers , name='modifCompteTiers'),
    path('supprimerCompteTiers/<int:emp_id>', views.supprimerCompteTiers , name='supprimerCompteTiers'),

    path('caisse/', views.caisse , name='caisse'),
    path('modifCaisse/', views.modifCaisse , name='modifCaisse'),
    path('supprimerCaisse/<int:emp_id>', views.supprimerCaisse , name='supprimerCaisse'),

    path('tiers/', views.tiers , name='tiers'),
    path('modifTiers/', views.modifTiers , name='modifTiers'),
    path('supprimerTiers/<int:emp_id>', views.supprimerTiers , name='supprimerTiers'),

    path('categorie/', views.categorie , name='categorie'),
    path('modifCategorie/', views.modifCategorie , name='modifCategorie'),
    path('supprimerCategorie/<int:emp_id>', views.supprimerCategorie , name='supprimerCategorie'),
    
    path('compteG/', views.compteG , name='compteG'),
    path('modifCompteG/', views.modifCompteG , name='modifCompteG'),
    path('supprimerCompteG/<int:emp_id>', views.supprimerCompteG , name='supprimerCompteG'),

    path('test2/', views.test2 , name='test2'),
    path('test1/', views.test1 , name='test1'),
    path('test0/', views.test0 , name='test0'),
    path('test11/', views.test11 , name='test11'),
    path('testeur/', views.testeur , name='testeur'),

    path('login/', views.login , name='login'),
    path('login2/', views.login2 , name='login2'),
    path('logout/', views.logout , name='logout'),
    path('login1/', views.login1 , name='login1'),
    path('home/', views.home , name='home'),
    path('brouillard/', views.brouillard , name='brouillard'),
    

    path('operation/', views.operation , name='operation'),

    path('operation1/', views.operation1 , name='operation1'),
    path('supprimerOP/<int:emp_id>', views.supprimerOP , name='supprimerOP'),
    path('modifOP/<int:emp_id>', views.modifOP , name='modifOP'),
    path('modifOP1/', views.modifOP1 , name='modifOP1'),
    path('modifierOP/', views.modifierOP , name='modifierOP'),
]