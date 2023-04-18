from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    # add any other fields you want to include in the registration form
