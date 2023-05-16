from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# creates the form to make a new user.
class BootstrapUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# creates the form to log in
class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# creates the form to update user account information
class UpdateUserForm(forms.ModelForm):
    birthdate = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    street_address = forms.CharField(max_length=255, required=True)
    zip_code = forms.CharField(max_length=10, required=True)
    state = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthdate', 'street_address', 'zip_code', 'state')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['birthdate'].initial = self.instance.profile.birthdate
            self.fields['street_address'].initial = self.instance.profile.street_address
            self.fields['zip_code'].initial = self.instance.profile.zip_code
            self.fields['state'].initial = self.instance.profile.state

    # saving the updated user information to the database
    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.birthdate = self.cleaned_data['birthdate']
        user.profile.street_address = self.cleaned_data['street_address']
        user.profile.zip_code = self.cleaned_data['zip_code']
        user.profile.state = self.cleaned_data['state']
        user.profile.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    pass
