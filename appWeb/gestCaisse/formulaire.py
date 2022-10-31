from dataclasses import fields
from django.forms import ModelForm
from .models import *
from django import forms

class Employee_form(ModelForm):
    class Meta:
        model = Employee
        fields ='__all__'

class Tier_form(ModelForm):
    class Meta:
        model = Tier
        fields='__all__'

class CompteTier_form(ModelForm):
    class Meta:
        model = CompteTier
        fields='__all__'

class Categorie_form(ModelForm):
    class Meta:
        model = Categorie
        fields='__all__'

class Caisse_form(ModelForm):
    class Meta:
        model = Caisse
        fields='__all__'

class Operation_form(ModelForm):
    class Meta:
        model = Operation
        fields='__all__'

class TestForm (forms.Form):
    tel = forms.CharField(label='Votre numero',max_length=20)
    nontant = forms.CharField(label='Le montant',max_length=20)