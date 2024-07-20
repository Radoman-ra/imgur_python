from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Image


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image", "title", "description"]
