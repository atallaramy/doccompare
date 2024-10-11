from django import forms


class FileUploadForm(forms.Form):
    file1 = forms.FileField(label="Select the first document")
    file2 = forms.FileField(label="Select the second document")
