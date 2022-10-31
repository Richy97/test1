from django.db import models

# Create your models here.
class Employee(models.Model): 
    matricule = models.CharField('matricule',max_length=50)
    nom = models.CharField('nom',max_length=200)
    prenom =models.CharField('prénom',max_length=200)
    email = models.CharField('E-mail',max_length=100)
    telephone = models.CharField('téléphone',max_length=50)
    login= models.CharField('login',max_length=50)
    password = models.CharField('password',max_length=50)
    fonction = models.CharField('fonction',max_length=200)
    

    def __str__(self):
        return self.login
class CompteG(models.Model):
    codeCaisse= models.CharField(max_length=100)
    numero=models.CharField(max_length=50)
    libele = models.CharField(max_length=50)
    natureCompte = models.CharField(max_length=50)
    
    def __str__(self):
        return self.numero

class Caisse(models.Model):
    codeCaisse= models.CharField(max_length=100)
    libele = models.CharField(max_length=100)
    typePaiement=models.CharField(max_length=50)
    soldeCaisse=models.IntegerField()
    devise=models.CharField(max_length=50)
    codeJournal=models.CharField(max_length=15)
    idCompteG = models.ForeignKey(CompteG, models.SET_NULL,blank=True,null=True,)
    def __str__(self):
        return self.libele



class Categorie(models.Model):
    codeCategorie= models.CharField(max_length=100)
    libele= models.CharField(max_length=100)
    sens = models.CharField(max_length=100)
    idCompteG = models.ForeignKey(CompteG, models.SET_NULL,blank=True,null=True,)
    saisieTier = models.CharField(max_length=100)
    def __str__(self):
        return self.codeCategorie


class CompteTier(models.Model):
    codeCompteTier= models.CharField(max_length=100)
    libele = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    idCompteG = models.ForeignKey(CompteG, models.SET_NULL,blank=True,null=True,)
    
    def __str__(self):
        return self.libele
    
class Tier(models.Model):
    codeTier = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telephone= models.CharField(max_length=50)
    localisation=models.CharField(max_length=200)
    idCT = models.ForeignKey(CompteTier, models.SET_NULL,blank=True,null=True,)


    def __str__(self):
        return self.nom


class EmployeCaisse(models.Model):
    idEmp = models.ForeignKey(Employee, models.SET_NULL,blank=True,null=True,)
    idCaisse = models.ForeignKey(Caisse, models.SET_NULL,blank=True,null=True,)
    date = models.DateTimeField('date published')


class Operation(models.Model):
    numOperation = models.CharField(max_length=50)
    MSISDN=models.CharField(max_length=50)
    montant = models.IntegerField()
    reference = models.CharField(max_length=50)
    numFacture = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    date = models.DateTimeField('date published')
    idEmp = models.ForeignKey(Employee, models.SET_NULL,blank=True,null=True,)
    idTier = models.ForeignKey(Tier, models.SET_NULL,blank=True,null=True,)
    idCaisse = models.ForeignKey(Caisse, models.SET_NULL,blank=True,null=True,)
    idCategorie= models.ForeignKey(Categorie, models.SET_NULL,blank=True,null=True,)
    
    def __str__(self):
        return self.numOperation

class VarSoldeCaisse(models.Model):
    date = models.DateTimeField('date published')
    soldeCaisse=models.IntegerField()
    idCaisse = models.ForeignKey(Caisse, models.SET_NULL,blank=True,null=True,)
    
    def __str__(self):
        return self.idCaisse

class EcritureComptable(models.Model):
    
    sens= models.CharField(max_length=50)
    idOperation= models.ForeignKey(Operation, models.SET_NULL,blank=True,null=True,)

class Paramettre(models.Model):
    nomSociete = models.CharField(max_length=50)
    operation= models.CharField(max_length=50)
    brouillard= models.CharField(max_length=50)
    employe= models.CharField(max_length=50)
    caisse= models.CharField(max_length=50)
    tiers= models.CharField(max_length=50)
    typeTiers= models.CharField(max_length=50)
    categorie= models.CharField(max_length=50)
    compteGeneral= models.CharField(max_length=50)
    theme= models.CharField(max_length=50)

