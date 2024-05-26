from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Prompt


class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ["name", "prompt"]

    def __init__(self, *args, **kwargs):
        super(PromptForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class InputForm(forms.Form):
    app_name = forms.CharField(max_length=100, required=True)
    root_folder = forms.CharField(max_length=100, required=False)
