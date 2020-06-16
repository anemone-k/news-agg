from django import forms

from .models import User, My_lenta

class UserCForm(forms.ModelForm):
   # should_publish = forms.Field(widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class LentaForm(forms.ModelForm):
    class Meta:
        model = My_lenta
        fields = ('ria', 'interfax', 'regnum', 'rt')