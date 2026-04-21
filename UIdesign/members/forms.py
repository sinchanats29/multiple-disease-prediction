from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class DiabetesForm(forms.Form):
    pregnancies = forms.FloatField()
    glucose = forms.FloatField()
    blood_pressure = forms.FloatField()
    skin_thickness = forms.FloatField()
    insulin = forms.FloatField()
    bmi = forms.FloatField()
    diabetes_pedigree_function = forms.FloatField()
    age = forms.IntegerField()
