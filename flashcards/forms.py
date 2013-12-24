from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    f  = forms.FileField()

class UploadForm(forms.Form):
    f  = forms.FileField()