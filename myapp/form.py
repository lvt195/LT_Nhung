from django import forms

class GenerateQRForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class ReadQRForm(forms.Form):
    image = forms.ImageField()
