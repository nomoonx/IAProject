__author__ = 'noMoon'
from django import forms

class crawlInitForm(forms.Form):
    hostSeeds=forms.CharField(label='hostSeeds')
    threadNumber=forms.CharField(label='threadNumber')