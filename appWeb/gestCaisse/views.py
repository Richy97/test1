from importlib.abc import SourceLoader
from turtle import width
from django.shortcuts import render,redirect
from .models import *
from .formulaire import *
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sessions.backends.db import SessionStore
import datetime
import json
import uuid
import random
import base64
import csv
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Table,TableStyle,Frame
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# Create your views here.
def index(request):    
    caisse=Caisse.objects.all() 
    return render(request,'gestCaisse/index.html',{'caisse':caisse})

def login(request):
    if request.method == 'POST':
        n=0
        date=timezone.now().strftime("%d-%m-%y")
        login=request.POST["login"]
        password=request.POST["password"]
        emp = Employee.objects.filter(login = login,password = password)
        for va in emp:
            if va.login==login and va.password==password:
                n= n+1
            else:
                n=n
        if n==1:
            emp1 = Employee.objects.get(login = login,password = password) 
            request.session['login'] = emp1.login
            request.session['password'] = emp1.password
            return redirect("/gestCaisse/")
        else:
            return render(request, 'gestCaisse/login.html', {})

    else:
        return render(request, 'gestCaisse/login.html', {})

def brouillards(request):
    login=request.session['login']
    password=request.session['password']
    emp1 = Employee.objects.get(login = login,password = password)   
    caisse=Caisse.objects.all() 
    
    if request.method == 'POST':
        caisse1 = request.POST['caisse']
        caisse2=Caisse.objects.get(codeCaisse = caisse1)
        debut1 = request.POST['debut']
        fin1 = request.POST['fin']
        form = Operation.objects.filter(idCaisse = caisse2 , date__gt = debut1 ,date__lte = fin1)
        form1 = EcritureComptable.objects.filter(idOperation=form)
    else:
        return redirect("/gestCaisse/")
    return render(request, 'gestCaisse/brouillards.html', {'emp1':emp1,'caisse':caisse,'form1':form1})

def operations(request):
    categorie=Categorie.objects.order_by()
    login=request.session['login']
    password=request.session['password']
    caisses=Caisse.objects.all()
    emp1 = Employee.objects.get(login = login,password = password)
    tier=Tier.objects.order_by()
    compteTier=CompteTier.objects.order_by() 
    if request.method == 'POST':
        caisse1 = request.POST['caisse']
        caisse=Caisse.objects.get(codeCaisse = caisse1)
        
        """  debut1 = request.POST['debut']
        fin1 = request.POST['fin']
        form1 = Operation.objects.filter(date__gt = debut1,date__lte = fin1) """
        form1 = Operation.objects.order_by('-date')
    else:
        caisse1 = request.session['caisse']
        caisse=Caisse.objects.get(codeCaisse = caisse1)
        form1 = Operation.objects.order_by('-date')
    
    return render(request, 'gestCaisse/operations.html', {'emp1':emp1,'tier':tier,'caisses':caisses,'caisse':caisse,'compteTier':compteTier,'categorie':categorie,'form1':form1})

def editOperation(request):
    
    return render(request, 'gestCaisse/editOperation.html', {})



################## Employé ##################################
def employe(request):
    login=request.session['login']
    password=request.session['password']
    emp1 = Employee.objects.get(login = login,password = password)
    caisse=Caisse.objects.all() 
    person = Employee.objects.order_by('matricule')
    if request.method == "POST":
        emp_nom = request.POST['nom']
        emp_prenom = request.POST['prenom']
        emp_email = request.POST['email']
        emp_telephone = request.POST['telephone']
        emp_fonction = request.POST['fonction']
        
        emp=Employee(nom=emp_nom,prenom=emp_prenom,email=emp_email,telephone=emp_telephone,fonction=emp_fonction)
        emp.save()
        return redirect('/gestCaisse/employe')
    else:
        emp = Employee_form()
    return render(request,'gestCaisse/employe.html',{'emp1':emp1,'caisse':caisse,'emp':emp,'person':person})

def modifEmp(request):
    matricule=request.POST['matricule']
    emp=Employee.objects.get(matricule=matricule)
    nom = request.POST['nom']
    prenom = request.POST['prenom']
    email = request.POST['email']
    telephone = request.POST['telephone']
    fonction = request.POST['fonction']
    emp.matricule=matricule
    emp.nom=nom
    emp.prenon=prenom
    emp.email=email
    emp.telephone=telephone
    emp.fonction=fonction
    emp.save()
    return redirect('/gestCaisse/employe/')  

def supprimerEmp(request,emp_id):
    emp = Employee.objects.get(pk=emp_id) 
    emp.delete()
    return redirect('/gestCaisse/employe/')
################## Caisse ##################################
def caisse(request):
    login=request.session['login']
    password=request.session['password']
    emp1 = Employee.objects.get(login = login,password = password)
    caisse=Caisse.objects.all() 
    compteG = CompteG.objects.order_by('id')
    caisses = Caisse.objects.order_by('libele')
    if request.method == "POST":
        caisse_libele = request.POST['libele']
        caisse_typePaiement = request.POST['typePaiement']
        caisse_soldeCaisse = request.POST['soldeCaisse']
        caisse_devise = request.POST['devise']
        caisse_codeJournal = request.POST['codeJournal']
        compteGeneral= request.POST['idCompteG']
        caisse_idCompteG = CompteG.objects.get(numero=compteGeneral)
        
        caisse=Caisse(libele=caisse_libele,typePaiement=caisse_typePaiement,soldeCaisse=caisse_soldeCaisse,devise=caisse_devise,codeJournal=caisse_codeJournal,idCompteG=caisse_idCompteG)
        caisse.save()
        return redirect('/gestCaisse/caisse')
    else:
        emp = Employee_form()
    return render(request,'gestCaisse/caisse.html',{'emp1':emp1,'caisse':caisse,'caisses':caisses,'compteG':compteG})

def modifCaisse(request):
    matricule=request.POST['libele']
    caisse=Caisse.objects.get(libele=matricule)
    caisse_libele = request.POST['libele']
    caisse_typePaiement = request.POST['typePaiement']
    caisse_soldeCaisse = request.POST['soldeCaisse']
    caisse_devise = request.POST['devise']
    caisse_codeJournal = request.POST['codeJournal']
    compteG = request.POST['idCompteG']
    caisse_idCompteG = CompteG.objects.get(numero=compteG)

    caisse.libele=caisse_libele
    caisse.codeJournal=caisse_codeJournal
    caisse.typePaiement=caisse_typePaiement
    caisse.soldeCaisse=caisse_soldeCaisse
    caisse.devise=caisse_devise
    caisse.idCompteG=caisse_idCompteG
    caisse.save()
    return redirect('/gestCaisse/caisse/') 

def supprimerCaisse(request,emp_id):
    caisse = Caisse.objects.get(pk=emp_id) 
    caisse.delete()
    return redirect('/gestCaisse/caisse/') 
################## Tiers ##################################
def tiers(request):
    login=request.session['login']
    password=request.session['password']
    emp1 = Employee.objects.get(login = login,password = password)
    caisse=Caisse.objects.all() 
    tiers = Tier.objects.order_by('id')
    compteTiers = CompteTier.objects.order_by('id')
    if request.method == "POST":
        tiers_codeTier=request.POST['codeT']
        tiers_nom = request.POST['nom']
        tiers_email = request.POST['email']
        tiers_telephone = request.POST['telephone']
        tiers_localisation = request.POST['localisation']
        compteT = request.POST['compteTiers']
        tiers_idCompteT = CompteTier.objects.get(numero=compteT)
        
        tier=Employee(codeTier=tiers_codeTier,nom=tiers_nom,email=tiers_email,telephone=tiers_telephone,localisation=tiers_localisation,idCT=tiers_idCompteT)
        tier.save()
        return redirect('/gestCaisse/employe')
    else:
        emp = Employee_form()
    return render(request,'gestCaisse/tiers.html',{'emp1':emp1,'caisse':caisse,'tiers':tiers,'compteTiers':compteTiers})

def modifTiers(request):
    tiers_codeTier=request.POST['codeT']
    tiers_nom = request.POST['nom']
    tiers_email = request.POST['email']
    tiers_telephone = request.POST['telephone']
    tiers_localisation = request.POST['localisation']
    compteT = request.POST['compteTiers']
    tiers_idCompteT = CompteTier.objects.get(numero=compteT)
    tiers=CompteTier.objects.get(libele=tiers_codeTier)

    tiers.codeTier=tiers_codeTier
    tiers.nom=tiers_nom
    tiers.email=tiers_email
    tiers.telephone=tiers_telephone
    tiers.localisation=tiers_localisation
    tiers.idCT=tiers_idCompteT
    tiers.save()
    return redirect('/gestCaisse/caisse/') 

def supprimerTiers(request,emp_id):
    tiers = tiers.objects.get(pk=emp_id) 
    tiers.delete()
    return redirect('/gestCaisse/caisse/') 
################## Compte Tiers ##################################
def compteTiers(request):
    login=request.session['login']
    password=request.session['password']
    emp1 = Employee.objects.get(login = login,password = password)
    compteTiers = CompteTier.objects.order_by('id')
    caisse=Caisse.objects.all() 
    if request.method == "POST":
        compteTiers_libele=request.POST['libele']
        compteTiers_description = request.POST['description']
        compteGeneral = request.POST['idCompteG']
        compteTiers_idCompteG = CompteG.objects.get(numero=compteGeneral)
        
        compteTiers=CompteTier(libele=compteTiers_libele,description=compteTiers_description,idCompteG=compteTiers_idCompteG)
        compteTiers.save()
        return redirect('/gestCaisse/employe')
    else:
        emp = Employee_form()
    return render(request,'gestCaisse/typeTiers.html',{'emp1':emp1,'caisse':caisse,'compteTiers':compteTiers})

def modifCompteTiers(request):
    compteTiers_libele=request.POST['libele']
    compteTiers_description = request.POST['description']
    compteGeneral = request.POST['idCompteG']
    compteTiers_idCompteG = CompteG.objects.get(numero=compteGeneral)
    compteTiers=CompteTier.objects.get(libele=compteTiers_libele)

    compteTiers.libele=compteTiers_libele
    compteTiers.description=compteTiers_description
    compteTiers.idCompteG=compteTiers_idCompteG
    compteTiers.save()
    return redirect('/gestCaisse/compteTiers/') 

def supprimerCompteTiers(request,emp_id):
    compteTiers = CompteTier.objects.get(pk=emp_id) 
    compteTiers.delete()
    return redirect('/gestCaisse/compteTiers/') 
################## Categorie ##################################
def categorie(request):
    login=request.session['login']
    password=request.session['password']
    emp1 = Employee.objects.get(login = login,password = password)
    caisse=Caisse.objects.all() 
    categorie = Categorie.objects.order_by('id')
    if request.method == "POST":
        categorie_codeCategorie=request.POST['codeCategorie']
        categorie_libele = request.POST['libele']
        categorie_sens = request.POST['sens']
        compteGeneral = request.POST['idCompteG']
        categorie_idCompteG = CompteG.objects.get(numero=compteGeneral)
        
        categorie=Categorie(codeCategorie=categorie_codeCategorie,libele=categorie_libele,sens=categorie_sens,idCompteG=categorie_idCompteG)
        Categorie.save()
        return redirect('/gestCaisse/categorie')
    else:
        emp = Employee_form()
    return render(request,'gestCaisse/categorie.html',{'emp1':emp1,'caisse':caisse,'categorie':categorie})

def modifCategorie(request):
    categorie_codeCategorie=request.POST['codeCategorie']
    categorie_libele = request.POST['libele']
    categorie_sens = request.POST['sens']
    compteGeneral = request.POST['idCompteG']
    compteTiers_idCompteG = CompteG.objects.get(numero=compteGeneral)
    categorie=Categorie.objects.get(codeCategorie=categorie_codeCategorie)

    categorie.codeCategorie=categorie_codeCategorie
    categorie.libele=categorie_libele
    categorie.sens=categorie_sens
    categorie.idCompteG=compteTiers_idCompteG
    categorie.save()
    return redirect('/gestCaisse/categorie/') 

def supprimerCategorie(request,emp_id):
    categorie = Categorie.objects.get(pk=emp_id) 
    categorie.delete()
    return redirect('/gestCaisse/categorie/')     
################## Categorie ##################################
def compteG(request):
    login=request.session['login']
    password=request.session['password']
    emp1 = Employee.objects.get(login = login,password = password)
    compteGeneral = CompteTier.objects.order_by('id')
    caisse=Caisse.objects.all() 
    if request.method == "POST":
        compteGeneral_libele=request.POST['libele']
        compteGeneral_description = request.POST['description']
        compteGeneral_natureCompte = request.POST['natureCompte']
        
        compteTiers=CompteG(libele=compteGeneral_libele,description=compteGeneral_description,idCompteG=compteGeneral_natureCompte)
        compteTiers.save()
        return redirect('/gestCaisse/compteG')
    else:
        emp = Employee_form()
    return render(request,'gestCaisse/compteGeneral.html',{'emp1':emp1,'caisse':caisse,'compteGeneral':compteGeneral})

def modifCompteG(request):
    compteGeneral_libele=request.POST['libele']
    compteGeneral_description = request.POST['description']
    compteGeneral_natureCompte = request.POST['natureCompte']
    compteGeneral=CompteG.objects.get(libele=compteGeneral_libele)

    compteGeneral.libele=compteGeneral_libele
    compteGeneral.description=compteGeneral_description
    compteGeneral.natureCompte=compteGeneral_natureCompte 
    compteGeneral.save()
    return redirect('/gestCaisse/compteG/') 

def supprimerCompteG(request,emp_id):
    compteG = CompteG.objects.get(pk=emp_id) 
    compteG.delete()
    return redirect('/gestCaisse/compteG/') 

################## Profile ##################################


def profile(request):
    emps = Employee.objects.all()
    if request.method == "POST":
        matricule = request.POST['']
        emp = Employee.objects.get(matricule=matricule)
        emp.login = request.POST['']
        emp.password = request.POST['']
        emp.save()
    else:
        return render(request,'gestCaisse/profile.html',{'emps':emps})
    return render(request,'gestCaisse/profile.html',{'emps':emps})

########################################################################################################################################################################

################## Ancien code ##################################
def index1(request):
    val = request.POST["login"]
    n = 0
    emp=Employee.objects.all()
    for va in emp:
        if va.login==val:
            n= n+1
        else:
            n=n
    if n>0:
        emp1=Employee.objects.get(login = val)
        emp2=int(emp1.id)
        form1=Operation.objects.all()
        date=timezone.now()
        b=1
        caisse2=Caisse.objects.all()
        b1=EmployeCaisse.objects.get(idEmp = emp2)
        b2=b1.idCaisse
        for vale in caisse2:
            caisse3=Caisse.objects.get(id = b) 
            if b2 == caisse3:
                b=b+1 
                e1=Caisse.objects.get(id = b)
                e2=e1.id
            else:
                n= n+1
        caisse1=e2
        caisse=Caisse.objects.get(id = caisse1)   
        
    else:
        redirect("/gestCaisse/")

    return render(request, 'gestCaisse/operation.html', {"caisse":caisse,"emp1":emp1,"form1":form1,"date":date})

#def operation(request):
   
#return render(request, 'gestCaisse/operation.html', {})

def login2(request):
    if request.method == 'POST':
        n=0
        date=timezone.now().strftime("%d-%m-%y")
        login=request.POST["login"]
        password=request.POST["password"]
        emp = Employee.objects.filter(login = login,password = password)
        for va in emp:
            if va.login==login and va.password==password:
                n= n+1
            else:
                n=n
        if n==1:
            emp1 = Employee.objects.get(login = login,password = password) 
            request.session['login'] = emp1.login
            request.session['password'] = emp1.password
            return render(request, 'gestCaisse/home.html', {'emp1':emp1,"date":date})
    else:
        return render(request, 'gestCaisse/login2.html', {})
        

def home(request):
    date=timezone.now().strftime("%d-%m-%y")
    login=request.session['login']
    password=request.session['password']
    emp1 = Employee.objects.get(login = login,password = password) 
    
    return render(request, 'gestCaisse/home.html', {'emp1':emp1,"date":date})

def login1(request):
    if request.method == 'POST':
        login=request.session['login']
        password=request.session['password']
        caisse1 = request.POST["caisse"]
        request.session["caisse"]=caisse1
        emp1 = Employee.objects.get(login = login,password = password)
        tier=Tier.objects.order_by()
        caisse=Caisse.objects.get(libele = caisse1)
        compteTier=CompteTier.objects.order_by()
        categorie=Categorie.objects.order_by() 
        form1 = Operation.objects.order_by('-date')[:7]
        
        return render(request, 'gestCaisse/operation.html', {'emp1':emp1,'tier':tier,'caisse':caisse,'compteTier':compteTier,'categorie':categorie,'form1':form1})
    else:
        return render(request, 'gestCaisse/login1.html', {})

def logout(request):
    try:
        del request.session['login']
        del request.session['password']
        del request.session['caisse']
    except KeyError:
        pass
    return redirect('/gestCaisse/login')

########################################################################################################################################################################

################## Operation de caisse ##################################

def operation(request):
    login=request.session['login']
    password=request.session['password']
    caisse1 = request.session["caisse"]
    emp1 = Employee.objects.get(login = login,password = password)
    tier=Tier.objects.order_by()
    caisse=Caisse.objects.get(libele = caisse1)
    compteTier=CompteTier.objects.order_by()
    categorie=Categorie.objects.order_by() 
    if request.method == 'POST':
        test = request.POST['test']
        
        if test == 'montant':
            mini1 = request.POST['min']
            maxi1 = request.POST['max']
            mini = int(mini1)
            maxi = int(maxi1)
            form1 = Operation.objects.filter(montant__gt=mini,montant__lte = maxi)
        else:
            debut1 = request.POST['debut']
            fin1 = request.POST['fin']
            
            form1 = Operation.objects.filter(date__gt = debut1,date__lte = fin1)
    else:
        
        form1 = Operation.objects.order_by('-date')[:7]
        
    return render(request, 'gestCaisse/operation.html', {'emp1':emp1,'tier':tier,'caisse':caisse,'compteTier':compteTier,'categorie':categorie,'form1':form1})

#insertion

def operation1(request):
    b=0
    choix1=request.POST['choix1']
    recu=request.POST['recu']
    choix=request.POST['choix']
    idEmp= request.POST['emp']
    opmontant1=request.POST['montant']
    opfacture=request.POST['facture']
    opmontant=int(opmontant1)
    
    categorie= request.POST['categorie']
    
    idCaisse= request.POST['caisse']
    request.session['caisse'] = idCaisse

    opdescription=request.POST['description']
    opidEmp1 =int(idEmp)
    opidCaisse1 = int(idCaisse)
    for e in Operation.objects.all():
        b = e.id
    nombre = str(b)
    opnumOperation ="OP"+nombre
    opMSISDN='0'
    opreference = request.POST['reference']
    opdate=timezone.now()
    
    opcategorie=Categorie.objects.get(codeCategorie=categorie)
    opidEmp =Employee.objects.get(pk=opidEmp1)
    opidCaisse = Caisse.objects.get(pk=opidCaisse1)

    solde=int(opmontant)
    solde1=int(opidCaisse.soldeCaisse)

    if opcategorie.sens =='Encaissement' :
        calcul= solde1 + solde
        opidCaisse.soldeCaisse = calcul
        opidCaisse.save()
        if choix=='oui' :
            idTier= request.POST['tier']
            opidTier =Tier.objects.get(nom=idTier)
            b1=Operation(numOperation=opnumOperation, MSISDN=opMSISDN, montant=opmontant, reference=opreference,numFacture=opfacture, description=opdescription,date=opdate,idEmp=opidEmp,idTier=opidTier,idCaisse =opidCaisse,idCategorie=opcategorie)
            b1.save()
        else:
            if choix1=='oui':
                b1=Operation(numOperation=opnumOperation, MSISDN=opMSISDN, montant=opmontant, reference=opreference,numFacture=opfacture, description=opdescription,date=opdate,idEmp=opidEmp,idCaisse =opidCaisse,idCategorie=opcategorie)
                b1.save()
            else:
                b1=Operation(numOperation=opnumOperation, MSISDN=opMSISDN, montant=opmontant, reference=opreference,numFacture=opfacture, description=opdescription,date=opdate,idEmp=opidEmp,idCaisse =opidCaisse,idCategorie=opcategorie)
                b1.save()
        
    else:
        if solde1 < solde:
            return HttpResponse('Votre solde est insuffisant')
        else:
            calcul= solde1 - solde
            opidCaisse.soldeCaisse = calcul
            opidCaisse.save()
            if choix=='oui' :
                idTier= request.POST['tier']
                opidTier =Tier.objects.get(nom=idTier)
                b1=Operation(numOperation=opnumOperation, MSISDN=opMSISDN, montant=opmontant, reference=opreference,numFacture=opfacture, description=opdescription,date=opdate,idEmp=opidEmp,idTier=opidTier,idCaisse =opidCaisse,idCategorie=opcategorie)
                b1.save()
            else:
                if choix1=='oui':
                  b1=Operation(numOperation=opnumOperation, MSISDN=opMSISDN, montant=opmontant, reference=opreference,numFacture=opfacture, description=opdescription,date=opdate,idEmp=opidEmp,idCaisse =opidCaisse,idCategorie=opcategorie)
                  b1.save()  
                else:
                    b1=Operation(numOperation=opnumOperation, MSISDN=opMSISDN, montant=opmontant, reference=opreference,numFacture=opfacture, description=opdescription,date=opdate,idEmp=opidEmp,idCaisse =opidCaisse,idCategorie=opcategorie)
                    b1.save()

    if recu=='oui':
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        doctitle='Piece de caisse'
        refEntreprise=["YIETO'O",'Integrateur de solutions informatique','22 avenue DeBrazza Bacongo','Brazzaville']
        tiers=''
        op=Operation.objects.get(numOperation=opnumOperation)
        entree=EcritureComptable(sens="Credit",idOperation=b1)
        entree1=EcritureComptable(sens="Debit",idOperation=b1)
        entree.save()
        entree1.save()
        textline=['Reference','numero compte general','numero compte tier','Description','Debit','Credit']
        salutation='Recevez, nos sinceres salutations.'
        service='service '

        pdf.drawInlineImage('gestCaisse/static/gestCaisse/Image/yietoo.jpg',20,760,width=200,height=80)
        text=pdf.beginText(20,750)
        for line in refEntreprise:
            text.textLine(line)
        pdf.drawText(text)
        pdf.drawCentredString(250,700,doctitle)
        pdf.line(208,699,292,699)

        pdf.drawString(40,650,'N* Piece')
        pdf.drawString(103,650,opnumOperation)
        pdf.drawString(100,650,':')
        

        pdf.drawString(40,630,'Description')
        pdf.drawString(103,630,opdescription)
        pdf.drawString(100,630,':')
        

        pdf.drawString(40,610,'Montant')
        pdf.drawString(103,610,opmontant1)
        pdf.drawString(100,610,':')
        

        pdf.drawString(500,760,opdate.strftime("%d-%m-%y"))
        
        

        pdf.drawString(20,450,salutation)
        pdf.drawString(40,560,'Caissier')
        pdf.drawString(250,560,'Beneficiere')
        pdf.drawString(450,560,'Direction')

        pdf.line(0,440,680,440)

        
        pdf.drawInlineImage('gestCaisse/static/gestCaisse/Image/yietoo.jpg',20,350,width=200,height=80)
        text=pdf.beginText(20,350)
        for line in refEntreprise:
            text.textLine(line)
        pdf.drawText(text)
        pdf.drawCentredString(250,280,doctitle)
        pdf.line(208,279,292,279)
        
        pdf.drawString(40,220,'N* Piece')
        pdf.drawString(105,220,opnumOperation)
        pdf.drawString(100,220,':')
        

        pdf.drawString(40,200,'Motif')
        pdf.drawString(105,200,opdescription)
        pdf.drawString(100,200,':')
        

        pdf.drawString(40,180,'Montant')
        pdf.drawString(105,180,opmontant1)
        pdf.drawString(100,180,':')
        

        pdf.drawString(500,360,opdate.strftime("%d-%m-%y"))
        
        

        pdf.drawString(20,20,salutation)
        pdf.drawString(40,130,'Caissier')
        pdf.drawString(250,130,'Beneficiere')
        pdf.drawString(450,130,'Direction')
        pdf.save()        
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='test2.pdf') 
    else:
        entree=EcritureComptable(sens="Credit",idOperation=b1)
        entree1=EcritureComptable(sens="Debit",idOperation=b1)
        entree.save()
        entree1.save()
    return redirect('/gestCaisse/operations/')

def supprimerOP(request,emp_id):
    op = Operation.objects.get(pk=emp_id) 
    op.delete()
    return redirect('/gestCaisse/operations/')

def modifierOP(request):
    iden=int(request.POST['id'])
    b1=Operation.objects.get(id=iden)
    idTier=request.POST['tier']
    opsens=request.POST['sens']
    solde21=b1.montant

    opmontant=request.POST['montant']
    opreference=request.POST['reference']
    opdescription=request.POST['description']
    opidTier=Tier.objects.get(nom=idTier) 
    opsens=Categorie.objects.get(codeCategorie = opsens) 
    montant=b1.idCaisse
    montant1=montant.id
    caisse=Caisse.objects.get(pk=montant1)
    montant2=caisse.soldeCaisse
    print(caisse)
    print(montant1)
    solde=int(opmontant)
    solde1=int(montant2)
    solde2=int(solde21)
    if opsens.libele =='Ecaissement' :
        calcul= solde1 + solde - solde2
        caisse.soldeCaisse = calcul
        caisse.save()
    else:
        calcul= solde1 - solde - solde2
        caisse.soldeCaisse = calcul
        caisse.save()

    if opsens.saisieTier == 'Oui':
        b1.montant=opmontant
        b1.reference=opreference
        b1.description=opdescription
        b1.idTier=opidTier
        b1.idCategorie=opsens
    else:
        b1.montant=opmontant
        b1.reference=opreference
        b1.description=opdescription
        b1.idCategorie=opsens
    b1.save()
    return redirect('/gestCaisse/operations/')  

def modifOP(request,emp_id):
    form =Operation.objects.get(pk=emp_id)
    categorie=Categorie.objects.all()
    tier=Tier.objects.all()
    typeTier=CompteTier.objects.all()
    return render(request, 'gestCaisse/modifOP.html', {'form': form, 'categorie': categorie,'tier': tier,'typeTier': typeTier}) 

def modifOP1(request):
    iden=int(request.POST['id'])
    b1=Operation.objects.get(id=iden)
    idTT=request.POST['typeTier']
    idTier=request.POST['tier']
    opsens=request.POST['sens']
    solde21=b1.montant

    opmontant=request.POST['montant']
    opreference=request.POST['reference']
    opdescription=request.POST['description']
    opidTT=CompteTier.objects.get(libele = idTT) 
    opidTier=Tier.objects.get(nom=idTier) 
    opsens=Categorie.objects.get(libele = opsens) 
    montant=b1.idCaisse
    montant1=montant.id
    caisse=Caisse.objects.get(pk=montant1)
    montant2=caisse.soldeCaisse
    print(caisse)
    print(montant1)
    solde=int(opmontant)
    solde1=int(montant2)
    solde2=int(solde21)
    if opsens.libele =='Encaissement' :
        calcul= solde1 + solde - solde2
        caisse.soldeCaisse = calcul
        caisse.save()
    else:
        calcul= solde1 - solde - solde2
        caisse.soldeCaisse = calcul
        caisse.save()
    b1.montant=opmontant
    b1.reference=opreference
    b1.description=opdescription
    b1.idCT=opidTT
    b1.idTier=opidTier
    b1.idCategorie=opsens

    b1.save()
    
    return redirect('/gestCaisse/operation/')
########################################################################################################################################################################

#Brouillard

def brouillard(request): 
    if request.method == 'POST':
        test = request.POST['test']
        
        if test == 'montant':
            mini1 = request.POST['min']
            maxi1 = request.POST['max']
            mini = int(mini1)
            maxi = int(maxi1)
            form1 = EcritureComptable.objects.filter(operation__montant__gt=mini,montant__lte = maxi,sens="Debit")
            form2 = EcritureComptable.objects.filter(operation__montant__gt=mini,montant__lte = maxi,sens="Credit")
            return render(request, 'gestCaisse/brouillard.html', {"form1":form1,"form2":form2})
        else:
            debut1 = request.POST['debut']
            fin1 = request.POST['fin']
            
            form1 = EcritureComptable.objects.filter(operation__date__gt = debut1,date__lte = fin1,sens="Debit")
            form2 = EcritureComptable.objects.filter(operation__date__gt = debut1,date__lte = fin1,sens="Credit")
            return render(request, 'gestCaisse/brouillard.html', {"form1":form1,"form2":form2})
    else:
        
        form1 = EcritureComptable.objects.order_by()
        return render(request, 'gestCaisse/brouillard.html', {"form1":form1})



########################################################################################################################################################################


########################################################################################################################################################################

def test1(request):
    caisse=Caisse.objects.all()
    emp1=Employee.objects.all()
    form1=EmployeCaisse.objects.all()
   
    return render(request, 'gestCaisse/test1.html', {"caisse":caisse,"emp1":emp1,"form1":form1})

def test2(request):
    form1 = Operation.objects.order_by('-date')[:7]
    return #render(request, 'gestCaisse/editable-table.html', {'form1':form1})

def test11(request):
    idEmp= request.POST['emp']
    idCaisse= request.POST['caisse']
    opdate=timezone.now()

    opidEmp1 =int(idEmp)
    opidCaisse1 = int(idCaisse)

    opidEmp =Employee.objects.get(pk=opidEmp1)
    opidCaisse = Caisse.objects.get(pk=opidCaisse1)

    b1=EmployeCaisse(idEmp=opidEmp,idCaisse=opidCaisse,date=opdate)
    b1.save()
   
    return render(request, 'gestCaisse/test1.html', {})

def test0(request):
    with open('eggs.csv', 'w', newline='') as csvfile:
        n=0
        spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Spam']+['Spam']+ ['Baked Beans'])
        while n<10:
            spamwriter.writerow(['Spam']+['Spam']+ ['Baked Beans'])
            n= n+1
    return HttpResponse('Reussi')

###########################################################################################################################################################################
def testeur(request):
    
    opdate=timezone.now()
    print(opdate.strftime("%d/%b/%y"))

    return HttpResponse(opdate.strftime("%d-%m-%y"))