from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CreateNewBasket(forms.Form):
    name = forms.CharField(label="Basket Name", max_length=200)

class RenameBasket(forms.Form):
    new_name = forms.CharField(label="New Basket Name", max_length=200)
