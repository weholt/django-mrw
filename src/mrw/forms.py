from django import forms


class InputForm(forms.Form):
    app_name = forms.CharField(max_length=100, required=True)
    root_folder = forms.CharField(max_length=100, required=False)
